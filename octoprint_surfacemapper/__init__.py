import octoprint.plugin

class SurfaceMapperPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin):
    def on_after_startup(self):
        self._logger.info("SurfaceMapper plugin started.")

__plugin_name__ = "SurfaceMapper"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = SurfaceMapperPlugin()
