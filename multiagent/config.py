
import yaml

# TODO: singleton
class Config:
    def __init__(self) -> None:
        with open("D:/config.yaml", 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                # openai_wrapper_base_url
                self.base_api_url = config['config']['BASE_API_URL']
                
            except yaml.YAMLError as exc:
                print(exc)

        self.rpm = 3

    def get(self,key,*args,**kwargs):
        pass