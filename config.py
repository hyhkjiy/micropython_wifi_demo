# -*- coding:utf-8 -*-
"""
基础配置文件
***重要***: 不依赖项目内任何模块
"""
import json


class ConfigFile(object):
    FileName = '/config.json'

    @staticmethod
    def load():
        try:
            with open(ConfigFile.FileName, 'r') as f:
                config = json.loads(f.read() or '{}')
            return config
        except OSError:
            return {}

    @staticmethod
    def get(*args, **kwargs):
        config = ConfigFile.load()
        return config.get(*args, **kwargs)

    @staticmethod
    def set(key, value):
        config = ConfigFile.load()
        config[key] = value
        with open(ConfigFile.FileName, 'w') as f:
            f.write(json.dumps(config))


if __name__ == '__main__':
    print(ConfigFile.get('a'))
    ConfigFile.set('a', True)
    print(ConfigFile.get('a'))
    ConfigFile.set('a', False)
    print(ConfigFile.get('a'))
