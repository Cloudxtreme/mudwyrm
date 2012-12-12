define([
    'ace/theme/clouds',
    'ace/theme/clouds_midnight',
    'ace/theme/cobalt',
    'ace/theme/dawn',
    'ace/theme/eclipse',
    'ace/theme/idle_fingers',
    'ace/theme/kr_theme',
    'ace/theme/mono_industrial',
    'ace/theme/monokai',
    'ace/theme/pastel_on_dark',
    'ace/theme/textmate',
    'ace/theme/twilight'
], function() {
    return {
        initialize: function() {
            var self = this;
            _.each(self, function(v, name) {
                if (typeof v === 'object' && self.get(name) === null) {
                    self.set(name, v.default);
                }
            });
        },
        get: function(name) {
            if (!localStorage[name])
                return null;
            return JSON.parse(localStorage[name]);
        },
        set: function(name, value) {
            localStorage[name] = JSON.stringify(value);
        },
        
        filetreeFolder: {
            default: ''
        },
        openTabs: {
            default: []
        },
        filenameFilter: {
            default: ['.pyc$']
        },
        theme: {
            default: 'twilight',
            options: {
                'clouds': {
                    label: 'Clouds',
                    module: 'ace/theme/clouds'
                },
                'clouds_midnight': {
                    label: 'Clouds Midnight',
                    module: 'ace/theme/clouds_midnight'
                },
                'cobalt': {
                    label: 'Cobalt',
                    module: 'ace/theme/cobalt'
                },
                'dawn': {
                    label: 'Dawn',
                    module: 'ace/theme/dawn'
                },
                'eclipse': {
                    label: 'Eclipse',
                    module: 'ace/theme/eclipse'
                },
                'idle_fingers': {
                    label: 'Idle Fingers',
                    module: 'ace/theme/idle_fingers'
                },
                'kr_theme': {
                    label: 'KR Theme',
                    module: 'ace/theme/kr_theme'
                },
                'mono_industrial': {
                    label: 'Mono Industrial',
                    module: 'ace/theme/mono_industrial'
                },
                'monokai': {
                    label: 'Monokai',
                    module: 'ace/theme/monokai'
                },
                'pastel_on_dark': {
                    label: 'Pastel on Dark',
                    module: 'ace/theme/pastel_on_dark'
                },
                'textmate': {
                    label: 'Textmate',
                    module: 'ace/theme/textmate'
                },
                'twilight': {
                    label: 'Twilight',
                    module: 'ace/theme/twilight'
                }
            }
        }
    };
});