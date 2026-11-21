# KirikiriLike — 配置项
#
# 本文件仅以库默认值声明可调项（位于 `kkl` 命名空间）。
# 只有当使用项目尚未设置某个配置项时，本文件才会为其应用默认值；
# 因此项目可在自己的 init（优先级 0）中预先设置任意值，库会尊重该值。
#
# 如何配置（在你的项目中配置，而不是在这里）：
#
#     init python:
#         kkl.enable_wheelnav = True        # 滚轮向上 = 历史，滚轮向下 = 推进
#         # 若要让头像感知说话人，请将 side_image_tag 保持为 None。
#
# 重要：请在默认 init 优先级（0）或任何低于 100 的优先级下设置配置项。
# 库会在 init 100+ 读取它们，因此在 100+ 设置的值会被忽略。

# 尽早创建命名空间，以便项目可以写入。
init -100 python:
    import types
    if not hasattr(store, "kkl"):
        store.kkl = types.SimpleNamespace()

# 在项目自身 init（优先级 0）运行前应用库默认值，
# 但仅应用于项目尚未提供值的位置。
init -1 python:

    def _kkl_default(name, value):
        if not hasattr(store.kkl, name):
            setattr(store.kkl, name, value)

    # --- 主开关 --------------------------------------------------------------
    # 滚轮向上打开历史，滚轮向下推进对话（并关闭历史）。
    _kkl_default("enable_wheelnav", True)
    # 允许下文所述的可选固定标签覆盖。
    _kkl_default("enable_side_image", True)
    # 应用内置的半透明渐变文本框和 Nunito 样式。
    # 采用可选启用，以免安装/升级 KirikiriLike 时意外替换项目现有的对话呈现。
    _kkl_default("enable_textbox_template", False)

    # --- 侧图 ----------------------------------------------------------------
    # 正常感知说话人的行为请保持此项为 None。此时 Ren'Py 使用当前 Character 的
    # image 属性，旁白没有头像。在此设置标签会刻意让头像在所有行都固定到该显示的
    # 立绘，包括旁白和其他角色说出的对话。
    _kkl_default("side_image_tag", None)

    # --- 滚轮导航 ------------------------------------------------------------
    _kkl_default("wheel_up_key", "mousedown_4")     # 向上滚动
    _kkl_default("wheel_down_key", "mousedown_5")   # 向下滚动

    # --- 历史（回想）界面 ----------------------------------------------------
    # 为 True 时，在最新条目处向下滚动会关闭历史（KiriKiri 式退出）。
    _kkl_default("history_closes_on_wheeldown", True)
    # 复用项目自带 history_*/game_menu_* 样式（True），或使用库自带的
    # kkl_history_* 回退样式（False，用于非标准 GUI）。
    _kkl_default("history_use_project_styles", True)

    # --- 文本框模板 ----------------------------------------------------------
    # 仅当 enable_textbox_template 为 True 时，这些设置才会影响自带 say 界面样式。
    # 项目可替换任意单个值，同时保留模板的其余部分。
    _kkl_default(
        "textbox_background",
        "KirikiriLike/gui/textbox_glass_gradient.svg",
    )
    _kkl_default("textbox_feather_edges", True)
    _kkl_default(
        "textbox_horizontal_edge_mask",
        "KirikiriLike/gui/textbox_edge_horizontal.svg",
    )
    _kkl_default(
        "textbox_vertical_edge_mask",
        "KirikiriLike/gui/textbox_edge_vertical.svg",
    )
    _kkl_default("textbox_background_opacity", 1.0)
    _kkl_default("textbox_fallback_background_color", "#010204c7")
    _kkl_default("textbox_on_small", True)
    _kkl_default(
        "textbox_font",
        "KirikiriLike/fonts/Nunito-Regular.ttf",
    )
    _kkl_default(
        "textbox_name_font",
        "KirikiriLike/fonts/Nunito-SemiBold.ttf",
    )
    _kkl_default("textbox_fallback_font", "DejaVuSans.ttf")
    _kkl_default("textbox_text_color", "#f7f9fc")
    _kkl_default("textbox_name_color", "#ffffff")
    # Ren'Py 描边元组格式为 (thickness, color, x offset, y offset)。
    # 大小 0 会让第一层成为字形阴影，而不是扩张的描边。其两像素向下偏移和
    # 40% 不透明度会在居中的一像素可读性描边下方留下一个可见阴影像素。
    _kkl_default(
        "textbox_text_outlines",
        [(0, "#00000066", 0, 2), (1, "#000000c0", 0, 0)],
    )
    _kkl_default(
        "textbox_name_outlines",
        [(0, "#00000066", 0, 2), (1, "#000000cc", 0, 0)],
    )
    # None 会移除独立姓名铭牌，使玻璃面板外观更干净。
    # 设置为 displayable 或图像路径可保留自定义姓名框背景。
    _kkl_default("textbox_namebox_background", None)

    # --- 回滚 ----------------------------------------------------------------
    # 库默认保留回滚可用（滚轮向上会在回滚绑定之前被捕获，因此无需禁用回滚
    # 即可打开历史）。设为 True 可像 KiriKiri 一样完全禁用回滚。
    _kkl_default("force_rollback_disabled", False)
