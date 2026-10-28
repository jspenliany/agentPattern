import random
from datetime import datetime, timedelta
import json

def get_user_orders(user_id):
    """
    查询用户近期的订单列表及商品信息（固定返回 10 条模拟订单数据）
    """
    # 模拟商品池，用于随机组合到订单中
    product_pool = [
        {"product_id": "P1001", "product_name": "iPhone 16 Pro", "price": 7999.00, "category": "数码"},
        {"product_id": "P1002", "product_name": " could 9 运动鞋", "price": 599.00, "category": "鞋服"},
        {"product_id": "P1003", "product_name": "机械键盘 (104键)", "price": 399.00, "category": "外设"},
        {"product_id": "P1004", "product_name": "挂耳咖啡 (24袋入)", "price": 89.00, "category": "食品"},
        {"product_id": "P1005", "product_name": "人体工学电脑椅", "price": 1299.00, "category": "家具"},
        {"product_id": "P1006", "product_name": "无线降噪耳机", "price": 1099.00, "category": "数码"},
        {"product_id": "P1007", "product_name": "保温杯 500ml", "price": 129.00, "category": "百货"},
        {"product_id": "P1008", "product_name": "全自动雨伞", "price": 49.00, "category": "百货"},
        {"product_id": "P1009", "product_name": "科幻小说《三体》全集", "price": 98.00, "category": "图书"},
        {"product_id": "P1010", "product_name": "智能手环 9代", "price": 269.00, "category": "数码"}
    ]

    statuses = ["已支付", "待发货", "已发货", "已完成"]
    orders = []

    # 固定生成 10 条数据
    for i in range(1, 11):
        # 随机选择 1~2 个商品放入该订单
        order_items = random.sample(product_pool, random.randint(1, 2))

        # 计算订单总金额和商品详情
        total_amount = 0
        items_detail = []
        for prod in order_items:
            quantity = random.randint(1, 2)
            total_amount += prod["price"] * quantity
            items_detail.append({
                "product_id": prod["product_id"],
                "product_name": prod["product_name"],
                "price": prod["price"],
                "category": prod["category"],
                "quantity": quantity
            })

        # 模拟近期的时间（最近30天内）
        random_days_ago = random.randint(0, 30)
        order_time = (datetime.now() - timedelta(days=random_days_ago)).strftime("%Y-%m-%d %H:%M:%S")

        # 组装订单对象
        order = {
            "order_id": f"ORD20261023{user_id:04d}{i:02d}",  # 基于日期、用户ID和序号生成
            "user_id": user_id,
            "order_time": order_time,
            "order_status": random.choice(statuses),
            "total_amount": round(total_amount, 2),
            "items": items_detail
        }
        orders.append(order)

    # 按订单时间从新到旧排序
    orders.sort(key=lambda x: x["order_time"], reverse=True)

    return orders


def get_logistics_status(order_id):
    """
    查询物流轨迹（固定返回模拟物流数据，并基于 order_id 保证状态的一致性）
    返回状态：在途、卡死超 3 天、已签收
    """
    import random
    from datetime import datetime, timedelta

    # --------- 1. 一致性确定机制 ---------
    # 使用 order_id 的哈希值作为随机种子，只要 order_id 相同，生成的物流轨迹和状态就完全一样
    seed_value = hash(order_id)
    rng = random.Random(seed_value)

    # --------- 2. 状态与轨迹路由 ---------
    # 随机决定当前订单的物流状态
    status_options = ["在途", "卡死超 3 天", "已签收"]
    current_status = rng.choice(status_options)

    # 模拟快递公司和快递单号
    express_companies = ["顺丰速运", "中通快递", "京东快递", "圆通速递"]
    company = rng.choice(express_companies)
    waybill_number = f"SF{rng.randint(1000000000, 9999999999)}"

    # 模拟网点城市池
    cities = ["深圳转运中心", "上海分拨中心", "北京集散点", "广州配送中心", "杭州中转站"]
    rng.shuffle(cities)

    # 基于当前时间向前推算物流节点的发生时间
    now = datetime.now()
    traces = []

    if current_status == "已签收":
        # 已签收：完整的物流链路
        t4 = now - timedelta(hours=rng.randint(2, 12))
        t3 = t4 - timedelta(hours=rng.randint(6, 18))
        t2 = t3 - timedelta(days=rng.randint(1, 2))
        t1 = t2 - timedelta(hours=rng.randint(4, 12))

        traces = [
            {"time": t1.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[0]}】包裹已打包，等待揽收"},
            {"time": t2.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[0]}】已发出，正发往【{cities[1]}】"},
            {"time": t3.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[1]}】已到达，派送员正在为您派件"},
            {"time": t4.strftime("%Y-%m-%d %H:%M:%S"), "station": "【已签收】您的包裹已由驿站/本人签收，感谢使用"}
        ]

    elif current_status == "卡死超 3 天":
        # 卡死超 3 天：最新的节点时间距离现在超过 72 小时
        days_ago = rng.randint(4, 7)  # 4~7天前卡住
        t2 = now - timedelta(days=days_ago)
        t1 = t2 - timedelta(hours=rng.randint(8, 24))

        traces = [
            {"time": t1.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[0]}】包裹已打包，顺丰已揽收"},
            {"time": t2.strftime("%Y-%m-%d %H:%M:%S"),
             "station": f"【{cities[0]}】已发出，正发往【{cities[1]}】（物流异常，请联系客服）"}
        ]

    else:  # 在途
        # 在途：最新的节点在不久前，仍在正常流转
        t3 = now - timedelta(hours=rng.randint(1, 5))
        t2 = t3 - timedelta(hours=rng.randint(12, 24))
        t1 = t2 - timedelta(hours=rng.randint(6, 12))

        traces = [
            {"time": t1.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[0]}】商家已发货"},
            {"time": t2.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[0]}】已发出，正发往【{cities[1]}】"},
            {"time": t3.strftime("%Y-%m-%d %H:%M:%S"), "station": f"【{cities[1]}】快件已到达分拨中心，准备发往下一站"}
        ]

    # 按时间从新到旧排序（符合用户查物流的习惯）
    traces.sort(key=lambda x: x["time"], reverse=True)

    # --------- 3. 组装返回数据 ---------
    return {
        "order_id": order_id,
        "logistics_company": company,
        "waybill_number": waybill_number,
        "current_status": current_status,
        "traces": traces
    }


def check_refund_policy(order_id, reason):
    """
    调取退款规则知识库，结合订单物流状态做出退款判决。
    通过复用 get_logistics_status 的逻辑，严格保证订单物流信息的一致性。

    退款规则：
    1. 如果物流状态为 "卡死超 3 天"（停滞超 48 小时），触发【丢件极速退款】规则，无需寄回。
    2. 如果物流状态为 "已签收"，触发【标准退货退款】规则，必须买家寄回。
    3. 如果物流状态为 "在途"，提示正在运输中，若执意退款需联系客服拦截快件。
    """
    # 1. 调用上一步的函数获取该订单的物流状态（该函数基于 order_id 哈希，已保证一致性）
    logistics = get_logistics_status(order_id)
    logistics_status = logistics["current_status"]

    # 2. 匹配知识库及退款决策逻辑
    decision = {}

    if logistics_status == "卡死超 3 天":
        decision = {
            "policy_applied": "丢件极速退款通道",
            "can_refund_instantly": True,
            "requires_return": False,
            "refund_instruction": "检测到该订单物流已停滞超过 48 小时，符合平台‘异常丢件极速退款’政策。系统已自动为您拦截该件，退款将在审核后原路退回，无需寄回商品。",
            "next_step": "等待系统自动原路退款"
        }

    elif logistics_status == "已签收":
        decision = {
            "policy_applied": "7天无理由/标准退货退款规则",
            "can_refund_instantly": False,
            "requires_return": True,
            "refund_instruction": "该商品已由驿站或本人签收。根据售后规则，您需要将商品打包完整并寄回商家网点。寄回时请勿到付，商品退回并验收入库后将为您处理退款。",
            "next_step": "请在售后页面填写寄回的快递单号"
        }

    else:  # 在途
        decision = {
            "policy_applied": "在途拦截与退款规则",
            "can_refund_instantly": False,
            "requires_return": False,
            "refund_instruction": "商品目前正处于正常运输状态。由于快件已发出，暂无法直接极速退款。我们将尝试为您联系快递公司进行在线拦截，若拦截成功将自动为您退款；若拦截失败，请在收到货后拒签或申请退货。",
            "next_step": "等待客服反馈拦截结果"
        }

    # 3. 组装返回的结构化数据
    return {
        "order_id": order_id,
        "user_reason": reason,
        "current_logistics_status": logistics_status,
        "decision": decision
    }


def apply_refund(order_id, amount, reason):
    """
    执行退款（高危操作：包含参数完整性校验、基于一致性策略的业务防刷校验、金额风控校验）
    """
    import random
    from datetime import datetime

    # ------------------ 1. 严格的基础参数校验 ------------------
    if not order_id or not isinstance(order_id, str):
        return {"success": False, "code": "INVALID_ORDER_ID", "msg": "订单号格式不正确或为空"}

    if not amount or not isinstance(amount, (int, float)) or amount <= 0:
        return {"success": False, "code": "INVALID_AMOUNT", "msg": "退款金额必须大于 0"}

    if not reason or not isinstance(reason, str) or len(reason).strip() < 4:
        return {"success": False, "code": "INVALID_REASON", "msg": "退款原因字数不足，请详细说明说明"}

    # ------------------ 2. 跨接口一致性校验 (风控核心) ------------------
    # 2.1 逆向解析 order_id 提取 user_id (基于上文格式: ORD20261023{user_id:04d}{i:02d})
    try:
        # 提取 user_id 部分并转为整数
        extracted_user_id = int(order_id[11:15])
    except (ValueError, IndexError):
        return {"success": False, "code": "ORDER_PARSE_ERROR", "msg": "非法的订单号格式"}

    # 2.2 通过 user_id 还原订单池，校验退款金额是否超出该订单的实际总金额
    user_orders = get_user_orders(extracted_user_id)
    matched_order = next((o for o in user_orders if o["order_id"] == order_id), None)

    if not matched_order:
        return {"success": False, "code": "ORDER_NOT_FOUND", "msg": "未找到对应的订单记录"}

    actual_total_amount = matched_order["total_amount"]

    # 金额溢出校验：退款金额绝对不能大于用户实际支付的订单总额
    if amount > actual_total_amount:
        return {
            "success": False,
            "code": "AMOUNT_OVERFLOW",
            "msg": f"退款金额({amount}元)超出该订单实际支付总额({actual_total_amount}元)，拒绝执行"
        }

    # 2.3 结合物流和退款策略库，校验退款路径是否合规
    policy_result = check_refund_policy(order_id, reason)
    logistics_status = policy_result["current_logistics_status"]
    policy_decision = policy_result["decision"]

    # ------------------ 3. 业务状态风控 ------------------
    # 如果已签收，但在执行退款时发现它走的是极速退款通道，或者由于前端篡改参数导致逻辑对不上，进行拦截
    if logistics_status == "已签收" and policy_decision["requires_return"]:
        # 模拟现实逻辑：已签收商品，若未检测到买家寄回的物流单号，拒绝直接打款
        # 在真实高危操作中，这里会去数据库查询售后单状态
        rng = random.Random(hash(order_id + "refund"))
        has_returned_waybill = rng.choice([True, False])  # 模拟买家是否填写了寄回单号

        if not has_returned_waybill:
            return {
                "success": False,
                "code": "RETURN_REQUIRED",
                "msg": "该订单已签收，请先在售后页面填写您寄回商品的快递单号，商家验收入库后方可退款"
            }

    # ------------------ 4. 执行退款（模拟打款成功） ------------------
    refund_no = f"REF{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"

    return {
        "success": True,
        "code": "REFUND_SUCCESS",
        "msg": "退款申请执行成功，资金已原路提交银行处理",
        "data": {
            "refund_no": refund_no,
            "order_id": order_id,
            "user_id": extracted_user_id,
            "refund_amount": round(amount, 2),
            "original_amount": actual_total_amount,
            "refund_channel": "微信支付/支付宝原路返回",
            "logistics_snapshot": logistics_status,
            "policy_snapshot": policy_decision["policy_applied"],
            "finish_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

tools = [get_user_orders, get_logistics_status, check_refund_policy, apply_refund]

# ---------- 测试调用 ----------
if __name__ == "__main__":
    # 假设查询用户 ID 为 888 的订单
    mock_orders = get_user_orders(user_id=888)

    print(f"成功获取到用户 888 的 {len(mock_orders)} 条伪造订单：\n")


    print(json.dumps(mock_orders, indent=4, ensure_ascii=False))
    test_id_1 = "ORD20261023088801"
    test_id_2 = "ORD20261023088802"

    print("--- 第一次查询订单 1 ---")
    print(json.dumps(get_logistics_status(test_id_1), indent=4, ensure_ascii=False))

    print("\n--- 第二次查询订单 1 (验证幂等性/一致性) ---")
    print(json.dumps(get_logistics_status(test_id_1), indent=4, ensure_ascii=False))

    print("\n--- 查询订单 2 (验证不同单号状态不同) ---")
    print(json.dumps(get_logistics_status(test_id_2), indent=4, ensure_ascii=False))

    # 使用相同的单号测试，它会继承上一步 get_logistics_status 的随机种子结果
    test_id_stuck = "ORD20261023088801"  # 如果上一步这个单号是卡死，这里必然走极速退款
    test_id_signed = "ORD20261023088802"  # 如果上一步这个单号是已签收，这里必然要求寄回
    print("--- 场景 1：申请退款（基于单号 1 对应物流状态） ---")
    result_1 = check_refund_policy(test_id_stuck, reason="物流一直不更新，不要了")
    print(json.dumps(result_1, indent=4, ensure_ascii=False))

    print("\n--- 场景 2：申请退款（基于单号 2 对应物流状态） ---")
    result_2 = check_refund_policy(test_id_signed, reason="不喜欢，尺码不合适")
    print(json.dumps(result_2, indent=4, ensure_ascii=False))

    # 1. 模拟从用户订单列表拿到了一个真实的订单号
    orders = get_user_orders(user_id=888)
    target_order = orders[0]
    target_id = target_order["order_id"]
    target_amount = target_order["total_amount"]

    print(f"模拟准备退款的目标订单: {target_id}, 订单总金额: {target_amount}元\n")

    # 2. 测试场景 A：金额黑客篡改校验（高风险行为）
    print("--- 场景 A：黑客尝试将退款金额改为 999999 元 ---")
    hack_result = apply_refund(order_id=target_id, amount=999999.00, reason="不想要了，申请退款")
    print(json.dumps(hack_result, indent=4, ensure_ascii=False))

    # 3. 测试场景 B：正常退款流（会根据该单号锁定的物流状态自动判定）
    print("\n--- 场景 B：正常发起实退金额退款 ---")
    normal_result = apply_refund(order_id=target_id, amount=target_amount, reason="商品不符合预期，申请售后")
    print(json.dumps(normal_result, indent=4, ensure_ascii=False))