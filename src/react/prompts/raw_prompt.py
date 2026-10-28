from src.react.tools.order_query import tools
from src.util.util_json import generate_tool_desc
from collections.abc import Sequence, Callable


def format_tool_call(tool_list: list) -> tuple[str, str]:
    tool_names: list = []
    tools_descriptions: str = """
1. get_user_orders:
   - 描述: 查询指定用户的近期购买订单列表及基本信息。
   - 参数: 
     - user_id (string, 必填): 用户的唯一标识ID，例如 "U1001"。

2. get_logistics_status:
   - 描述: 查询某个具体订单的最新物流轨迹与状态。
   - 参数: 
     - order_id (string, 必填): 订单编号，例如 "ORD2024030101"。

3. check_refund_policy:
   - 描述: 查询退款合规政策。根据物流状态和退款原因，判断是否允许极速退款。
   - 参数: 
     - order_id (string, 必填): 订单编号。
     - reason (string, 必填): 用户申请退款的原因，例如 "物流停滞", "商品损坏", "不想要了"。

4. apply_refund:
   - 描述: 【高危操作】向财务系统提交退款申请并退款给用户。调用此接口前，必须先确保已确认订单金额并符合退款政策。
   - 参数: 
     - order_id (string, 必填): 订单编号。
     - amount (number, 必填): 退款金额（元），必须大于0。
     - reason (string, 必填): 审核通过的退款原因说明。
"""
    for tool in tool_list:
        tool_names.append(tool["name"])

    return "".join(tool_names), tools_descriptions

def tool_description_automation(tool_obj: Sequence[Callable]) -> tuple[str, list]:
    tool_names: list = []
    tools_descriptions: str = ""
    for tool in tool_obj:
        tmp_tool_name, tmp_tool_description, tmp_tool_sig = generate_tool_desc(tool)
        tool_names.append(tmp_tool_name)
        tools_descriptions = tools_descriptions + tmp_tool_description
    return tools_descriptions, tool_names

def get_agent_prompt(tool_list: list) -> str:

    tool_names, tools_description = format_tool_call(tool_list)

    system_prompt = f"""Answer the following questions as best you can. You have access to the following tools:
{tools_description}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""

    return system_prompt

tool_list: list[str] = ["get_user_orders", "get_logistics_status", "check_refund_policy", "apply_refund"]
