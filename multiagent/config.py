
import os
import yaml

# TODO: singleton
class Config:

    default_yaml_file = "D:/config.yaml"

    def __init__(self,yaml_file=default_yaml_file) -> None:
        self._configs = {}
        self._init_with_config_files_and_env(self._configs,yaml_file)

        # self.rpm = 3
        self.openai_api_rpm = self._get('RPM', 3)
        self.openai_api_model = self._get('OPENAI_API_MODEL', "gpt-4")
        self.max_tokens_rsp = self._get('MAX_TOKENS', 2048)
        self.max_budget = self._get('MAX_BUDGET', 10)
        self.total_cost = 0.0

    def _init_with_config_files_and_env(self,configs:dict,yaml_file:str):
        # configs.update(os.environ)

        for _yaml_file in [yaml_file]:
            # print(_yaml_file)
            if not os.path.isfile(_yaml_file):
                continue
            
            with open(_yaml_file, 'r') as stream:
                yaml_data = yaml.safe_load(stream)
                if not yaml_data:
                    continue
                configs.update(yaml_data)


    def _get(self, *args, **kwargs):
        return self._configs.get(*args, **kwargs)
    
    def get(self, key, *args, **kwargs):
        value = self._get(key, *args, **kwargs)
        if value is None:
            raise ValueError(f"Key '{key}' not found in environment variables or in the YAML file")
        return value


if __name__ == "__main__":
    config = Config()
    print(config.openai_api_rpm)
    print(config._configs)