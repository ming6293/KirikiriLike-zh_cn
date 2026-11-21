# KirikiriLike — 核心接线
#
# 读取配置项（由项目在 init 0 设置）并应用引擎配置。
# 在 init 100 运行，以便项目提供的值已经就位。

init 100 python:

    # 可选固定标签覆盖。正常情况下此项保持为 None，让 Ren'Py 内置
    # SideImage() 只跟随当前 Character(image=...)。
    # 非 None 值会刻意让头像在每一行都跟随该显示的立绘，包括旁白。
    if kkl.enable_side_image and kkl.side_image_tag is not None:
        config.side_image_tag = kkl.side_image_tag

    # 可选的 KiriKiri 式硬性禁用回滚（默认关闭）。
    if kkl.force_rollback_disabled:
        config.rollback_enabled = False
