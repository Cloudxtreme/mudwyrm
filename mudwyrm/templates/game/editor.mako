<%inherit file="/base.mako"/>

<%def name="stylesheets()">
  ${self.stylesheet_link('editor.css')}
  ${parent.stylesheets()}
</%def>

<%def name="scripts()">
  ${parent.scripts()}
  <script>
    require({
            baseUrl: '/js',
            paths: {
                'ace': 'libs/ace',
                'pilot': 'libs/pilot',
                'cockpit': 'libs/cockpit'
            },
        },
        ['editor/main',
         'libs/underscore-min',
         'order!libs/jquery-1.5.2.min',
         'order!libs/jquery.contextMenu',
         'order!libs/jquery.simplemodal.1.4.1.min',
         'pilot/plugin_manager',
         'pilot/settings',
         'pilot/environment'],
        function(Editor) {
            $(function() {
                var catalog = require('pilot/plugin_manager').catalog;
                catalog.registerPlugins([
                    'pilot/index',
                    'cockpit/index',
                    'ace/defaults'
                ]).then(function() {
                    var env = require('pilot/environment').create();
                    catalog.startupPlugins({env: env}).then(function() {
                        var editor = new Editor("/user/${user_name}/");
                        editor.openTab("${file_path}", false);
                    });
                });
            });
        }
    );
  </script>
</%def>

<%def name="header()">
  <menu id="toolbar">
    <command id="save" label="Save"/>
  </menu>
  <menu id="tabs"></menu>
</%def>

<div id="sidebar">
  <select id="filetree_folder"></select>
  <ul id="filetree"></ul>
</div>
<div id="editor"></div>

<div id="save_confirm">
  <p>Do you want to save changes to <output id="filename">this file</output>?</p>
  <div id="buttons">
    <a id="discard" href="#">Don't save</a>
    <a id="cancel" href="#">Cancel</a>
    <a id="save" href="#">Save</a>
  </div>
</div>