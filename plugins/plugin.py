import os


class Plugin:
    enabled_plugins = []

    def loadPlugins(self):
        print('插件加载中')
        for filename in os.listdir("plugins/enabled_plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            self.enabled_plugins.append(filename)
        print(f'共加载到{len(self.enabled_plugins)}个插件')

    def runPlugin(self,**kwarg):
        for i in self.enabled_plugins:
            pluginName = os.path.splitext(i)[0]
            plugin = __import__('plugins.enabled_plugins.'+pluginName, fromlist=[pluginName])
            plugin.run(kwarg)

