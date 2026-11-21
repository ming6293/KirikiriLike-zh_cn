# KirikiriLike — 滚轮导航
#
# 重新利用鼠标滚轮：
#   * 滚轮向上   -> 打开历史（回想）界面
#   * 滚轮向下 -> 推进当前对话
#
# 滚轮向上在始终显示的 overlay 界面上使用 `key ... capture True`，因此会在默认
# 回滚绑定（config.underlay）之前被消耗。这意味着打开历史无需从
# config.keymap['rollback'] 移除 mousedown_4，也无需禁用回滚——键盘/PageUp 回滚
# 仍然可用。
#
# 滚轮向下通过引擎内置的 "dismiss" 键符推进（没有独立的 "advance" 界面动作），
# 并加入 config.keymap['dismiss']。它只会推进 say/pause 交互，不影响回滚。

screen kkl_wheelnav():
    zorder 90

    if kkl.enable_wheelnav:
        # 打开回想，抢先于默认回滚绑定。
        key kkl.wheel_up_key action ShowMenu("history") capture True


init 150 python:
    if kkl.enable_wheelnav:
        # 在游戏内交互期间显示滚轮向上捕获 overlay。
        if "kkl_wheelnav" not in config.overlay_screens:
            config.overlay_screens.append("kkl_wheelnav")

        # 滚轮向下通过内置 dismiss 行为推进对话。
        if kkl.wheel_down_key not in config.keymap["dismiss"]:
            config.keymap["dismiss"].append(kkl.wheel_down_key)
