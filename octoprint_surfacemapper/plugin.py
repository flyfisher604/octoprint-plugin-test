import octoprint.plugin

class SurfaceMapperPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.AssetPlugin
):
    def on_after_startup(self):
        self._logger.info("SurfaceMapper plugin started")
    
    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", name="SurfaceMapper")
        ]

    def get_assets(self):
        return {
            "js": ["js/surfacemapper.js"],
            "css": [],
            "less": []
        }
