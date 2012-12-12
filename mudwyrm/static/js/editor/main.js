define([
    './options',
    'ace/mode/text',
    'ace/mode/python',
    'ace/mode/javascript',
    'ace/mode/html',
    'ace/mode/css',
    'ace/mode/ruby',
    //'ace/keyboard/keybinding/vim',
    'ace/editor',
    'ace/edit_session',
    'ace/undomanager',
    'ace/virtual_renderer',
    'pilot/canon'
],
function(Options) {
    var AceEditor = require('ace/editor').Editor,
        AceEditSession = require('ace/edit_session').EditSession,
        AceUndoManager = require('ace/undomanager').UndoManager,
        AceRenderer = require('ace/virtual_renderer').VirtualRenderer,
        //AceVim = require('ace/keyboard/keybinding/vim').Vim,
        Canon = require('pilot/canon');
    
    var modePatterns = [
        {
            patterns: ["\.py$"],
            Mode: require('ace/mode/python').Mode
        },
        {
            patterns: ["\.js$"],
            Mode: require('ace/mode/javascript').Mode
        },
        {
            patterns: ["\.html$", "\.htm$", "\.mako$"],
            Mode: require('ace/mode/html').Mode
        },
        {
            patterns: ["\.css$"],
            Mode: require('ace/mode/css').Mode
        },
        {
            patterns: ["\.rb$"],
            Mode: require('ace/mode/ruby').Mode
        }
    ];
    
    var contextMenuOptions = {
        showMenu: function(element) {
            element.addClass('context_menu_open');
        },
        hideMenu: function(element) {
            element.removeClass('context_menu_open');
        }
    };
    
    function pathJoin(a, b) {
        if (a[a.length - 1] == '/')
            a = a.substring(0, a.length - 1);
        if (b[0] == '/')
            b = b.substring(1);
        return a + '/' + b;
    }
    
    var Editor = function(rootPath) {
        Options.initialize();
        
        var self = this;
        self.rootPath = rootPath;
        self.sessions = {};
        self.currentSessionPath = null;
        
        self.editor = new AceEditor(
            new AceRenderer($('#editor')[0]));
        self.editor.setTheme(Options.theme.options[Options.get('theme')].module);
        //self.editor.setKeyboardHandler(AceVim);
        
        addEventListener('popstate', function(e) {
            var path = location.pathname.split('/');
            path.pop();
            path = path.join('/');
            self.openTab(path, false);
        });
        
        $('#toolbar #save').click(function() {
            if (self.currentSessionPath) {
                self.saveTab(self.currentSessionPath);
            }
        });
        
        Canon.addCommand({
            name: 'save',
            bindKey: {
                win: 'Ctrl-S',
                mac: 'Command-S',
                sender: 'editor'
            },
            exec: function() {
                if (self.currentSessionPath) {
                    self.saveTab(self.currentSessionPath);
                }
            }
        });
        
        self.setFiletreeFolder(Options.get('filetreeFolder'));
        _.each(Options.get('openTabs'), function(tab) {
            self.openTab(tab, false);
        });
    };
    
    (function() {
        this.openTab = function(path, modifyHistory) {
            modifyHistory = modifyHistory || true;
            var self = this;
            if (path in this.sessions)
            {
                self._activateSession(path, modifyHistory);
            }
            else
            {
                var session = new AceEditSession("");
                session.loading = true;
                session.modified = false;
                
                var m = _.detect(modePatterns, function(a) {
                    return _.any(a.patterns, function(pattern) {
                        return path.search(pattern) >= 0;
                    });
                });
                if (m)
                    session.setMode(new m.Mode());
                session.setUndoManager(new AceUndoManager());
                    
                var tab = $('<li/>', {
                    click: function(e) {
                        e.preventDefault();
                        if (e.which === 1) {
                            self.openTab(path);
                        }
                        else if (e.which === 2) {
                            self.closeTab(path);
                        }
                    }
                }).appendTo($('#tabs'));
                $('<a/>', {
                    href: pathJoin(path, '/edit'),
                    text: path.split('/').pop()
                }).appendTo(tab);
                
                tab.contextMenu('tab_context_menu', {
                    'Close': {
                        click: function(element) {
                            self.closeTab(path);
                        }
                    },
                    'Close others': {
                        click: function(element) {
                            
                        }
                    },
                    'Save': {
                        click: function(element) {
                            self.saveTab(path);
                        }
                    }
                });
                
                session.tab = tab;
                self.sessions[path] = session;
                self._activateSession(path, modifyHistory);
                
                $.ajax({
                    url: path,
                    cache: false,
                    success: function(data) {
                        session.setValue(data);
                        session.on('change', function() {
                            tab.addClass('modified');
                            session.modified = true;
                        });
                        session.loading = false;
                        if (self.currentSessionPath === path) {
                            self.editor.setReadOnly(false);
                        }
                    }
                });
            }
        };
        
        this.closeTab = function(path) {
            var self = this,
                session = self.sessions[path];
            if (!session || session.loading)
                return;
            if (session.modified) {
                $('#save_confirm').modal({
                    position: ["20%"],
                    overlayId: 'save_confirm_overlay',
                    containerId: 'save_confirm_container',
                    onShow: function (dialog) {
                        $('#cancel', dialog.data[0]).click(function(e) {
                            e.preventDefault();
                            $.modal.close();
                        });
                        $('#discard', dialog.data[0]).click(function(e) {
                            e.preventDefault();
                            self._removeSession(path);
                            $.modal.close();
                        });
                        $('#save', dialog.data[0]).click(function(e) {
                            e.preventDefault();
                            self.saveTab(path);
                            self._removeSession(path);
                            $.modal.close();
                        });
                    }
                });
            }
            else {
                self._removeSession(path);
            }
        };
        
        this.saveTab = function(path) {
            var self = this,
                session = self.sessions[path];
            if (!session || session.loading)
                return;
            $.ajax({
                type: 'POST',
                url: pathJoin(path, '/edit'),
                data: {contents: session.getValue()},
                success: function(response) {
                    session.tab.removeClass('modified');
                    session.modified = false;
                }
            });
        };
        
        this.setFiletreeFolder = function(path) {
            var self = this;
            Options.set('filetreeFolder', path);
            if (path.indexOf(self.rootPath) === 0)
                path = path.substring(self.rootPath.length);
            $('#filetree').html('');
            self.refreshFiletreeFolder(pathJoin(self.rootPath, path),
                                       $('#filetree'));
            $('#filetree_folder').change(function() {
                self.setFiletreeFolder(
                    $('#filetree_folder option:selected').val());
            });
            $('#filetree_folder').html('');
            var currentPath = self.rootPath,
                addItem = function(name) {
                    currentPath = pathJoin(currentPath, name);
                    $('#filetree_folder').prepend(
                        $('<option/>', {
                            text: name ? name : "(root)",
                            value: currentPath
                        })
                    );
                }
            addItem('');
            if (path) {
                _.each(path.split('/'), addItem);
            }
        };
        
        function filenameFiltered(filename) {
            return _.any(
                Options.get('filenameFilter'),
                function(pattern) {
                   return new RegExp(pattern).test(filename)
                }
            );
        }
        
        this.refreshFiletreeFolder = function(path, element) {
            var self = this;
            $.getJSON(path + '/list', function(files) {
                var previous = null;
                element.children('.loading').remove();
                _.each(files, function(file) {
                    if (filenameFiltered(file.name))
                        return;
                    var existing = element.children('li').filter(function() {
                        return $(this).hasClass(file.type)
                            && $(this).children('a:first-child').text() === file.name;
                    });
                    if (existing.length) {
                        previous = existing;
                        return;
                    }
                    var li = $('<li/>', {
                        'class': file.type
                    });
                    if (previous) {
                        li.insertAfter(previous);
                    }
                    else {
                        li.appendTo(element);
                    }
                    previous = li;
                    
                    if (file.type === 'dir') {
                        var ul = $('<ul/>', {
                            'class': 'folded'
                        });
                        $('<a/>', {
                            href: file.path + '/list',
                            text: file.name,
                            click: function(e) {
                                e.preventDefault();
                                if (ul.hasClass('folded')) {
                                    ul.removeClass('folded');
                                    if (ul.children().length === 0) {
                                        ul.append($('<li/>', {
                                            'class': 'loading',
                                            text: 'Loading...'
                                        }));
                                    }
                                    self.refreshFiletreeFolder(file.path, ul);
                                }
                                else {
                                    ul.addClass('folded');
                                }
                            }
                        }).appendTo(li);
                        ul.appendTo(li);
                        
                        li.contextMenu('folder_context_menu', {
                            'Expand/collapse': {},
                            'Make this folder root': {
                                click: function(element) {
                                    self.setFiletreeFolder(file.path);
                                }
                            }
                        }, contextMenuOptions);
                    }
                    else {
                        $('<a/>', {
                            href: file.path + '/edit',
                            text: file.name,
                            click: function(e) {
                                e.preventDefault();
                                self.openTab(file.path);
                            }
                        }).appendTo(li);
                        li.contextMenu('file_context_menu', {
                            'Open': {
                                click: function(element) {
                                    self.openTab(file.path);
                                }
                            }
                        }, contextMenuOptions);
                    }
                });
            });
        };
        
        this._activateSession = function(path, modifyHistory) {
            var self = this;
            if (self.currentSessionPath === path)
                return;
            self.editor.setSession(self.sessions[path]);
            self.editor.setReadOnly(self.sessions[path].loading);
            if (self.currentSessionPath)
                self.sessions[self.currentSessionPath].tab.removeClass('selected');
            self.sessions[path].tab.addClass('selected');
            if (modifyHistory) {
                history.pushState(null, null, path + '/edit');
            }
            document.title = path.split('/').pop();
            self.currentSessionPath = path;
            Options.set('openTabs', _.keys(self.sessions));
        };
        
        this._removeSession = function(path) {
            var self = this;
            if (self.currentSessionPath === path) {
                var sessionPaths = _.keys(self.sessions),
                    currentIndex = _.indexOf(sessionPaths, path),
                    newIndex;
                if (sessionPaths.length <= 1)
                    return;
                if (currentIndex === sessionPaths.length - 1) {
                    newIndex = currentIndex - 1;
                }
                else {
                    newIndex = currentIndex + 1;
                }
                self._activateSession(sessionPaths[newIndex]);
            }
            self.sessions[path].tab.remove();
            delete self.sessions[path];
            Options.set('openTabs', _.keys(self.sessions));
        };
    }).call(Editor.prototype);
    
    return Editor;
});