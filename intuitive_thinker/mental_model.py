from intuitive_thinker.model_think_cot_reflect_prompt import think_cot_reflect_system_message, think_cot_reflect_userinput
from intuitive_thinker.model_thinking_fast_and_slow_prompt import (
    thinking_fast_and_slow_system_message, thinking_fast_and_slow_userinput, two_systems_thinking_system_message, two_systems_thinking_userinput)
from intuitive_thinker.model_cirtical_thinking_prompt import critical_thinking_system_message, critical_thinking_userinput
from intuitive_thinker.model_stocks_and_flows_prompts import stocks_and_flow_system_message, stocks_and_flow_userinput
from intuitive_thinker.model_second_order_thinking_prompts import second_order_thinking_system_message, second_order_thinking_userinput
from intuitive_thinker.model_nonlinear_prompts import model_nonlinear_system_thinking, model_nonlinear_userinput
from intuitive_thinker.model_iceberg_prompts import iceberg_thinking_system_message, iceberg_thinking_userinput
import json

# lookup mental models


def apply_thinking_model(model: str, query: str) -> str:
    print("...use thinking_model("+model+","+query+")\n")
    mental_models = {
        'chain_of_thoughts': {'system_message': think_cot_reflect_system_message,
                              'user_input': think_cot_reflect_userinput.format(userinput=query)},
        'thinking_fast_and_slow': {'system_message': thinking_fast_and_slow_system_message,
                                   'user_input': thinking_fast_and_slow_userinput.format(userinput=query)},
        'two_systems_thinking': {'system_message': two_systems_thinking_system_message,
                                 'user_input': two_systems_thinking_userinput.format(userinput=query)},
        'critical_thinking': {'system_message': critical_thinking_system_message,
                              'user_input': critical_thinking_userinput.format(userinput=query)},
        'stocks_and_flows_thinking': {'system_message': stocks_and_flow_system_message,
                                      'user_input': stocks_and_flow_userinput.format(userinput=query)},
        'second_order_thinking': {'system_message': second_order_thinking_system_message,
                                  'user_input': second_order_thinking_userinput.format(userinput=query)},
        'nonlinear_thinking': {'system_message': model_nonlinear_system_thinking,
                               'user_input': model_nonlinear_userinput.format(userinput=query)},
        'iceberg_thinking': {'system_message': iceberg_thinking_system_message,
                             'user_input': iceberg_thinking_userinput.format(userinput=query)},
    }
    return json.dumps(mental_models.get(model, {'error': 'mental model not found'}))


class MentalModel:
    # list of system thinking models
    CHAIN_OF_THOUGHTS = "chain_of_thoughts"
    CRTICAL_THINKING = "critical_thinking"
    THINKING_FAST_N_SLOW = "thinking_fast_and_slow"
    TWO_SYSTEMS_THINKING = "two_systems_thinking"
    STOCKS_AND_FLOWS_THINKING = "stocks_and_flows_thinking"
    SECOND_ORDER_THINKING = "second_order_thinking"
    NON_LINEAR_THINKING = "nonlinear_thinking"
    ICERBERG_THINKING = "iceberg_thinking"

    def __init__(self, model):
        self.model = model

    def __call__(self, query: str):
        self.query = query
        model_info = apply_thinking_model(self.model, self.query)
        return model_info
