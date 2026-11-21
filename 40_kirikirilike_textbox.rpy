# KirikiriLike - 可选的半透明渐变文本框模板
#
# 这会修改 Ren'Py 自带 say 界面使用的标准 window/namebox/say 样式。
# 它刻意不替换 screen say，因此 SideImage()、自定义快捷菜单和正常对话行为
# 仍由项目掌控。

init 105 python:

    def _kkl_textbox_template_active():
        return (
            kkl.enable_textbox_template
            and (kkl.textbox_on_small or not renpy.variant("small"))
        )

    def _kkl_textbox_resolve_font(value):
        # FontGroup 和其他字体对象本身已是有效的样式值。
        if not isinstance(value, str):
            return value

        if renpy.loadable(value):
            return value

        return kkl.textbox_fallback_font

    def _kkl_textbox_window_properties():
        if not _kkl_textbox_template_active():
            return {}

        source = kkl.textbox_background

        if isinstance(source, str) and not renpy.loadable(source):
            background = Solid(kkl.textbox_fallback_background_color)
        else:
            background = Frame(source, 0, 0, tile=False)

        if kkl.textbox_feather_edges:
            masks = (
                kkl.textbox_horizontal_edge_mask,
                kkl.textbox_vertical_edge_mask,
            )

            for mask_source in masks:
                if isinstance(mask_source, str) and not renpy.loadable(mask_source):
                    continue

                background = AlphaMask(
                    background,
                    Frame(mask_source, 0, 0, tile=False),
                )

        if kkl.textbox_background_opacity != 1.0:
            background = Transform(
                background,
                alpha=kkl.textbox_background_opacity,
            )

        return {"background": background}

    def _kkl_textbox_namebox_properties():
        if not _kkl_textbox_template_active():
            return {}

        return {"background": kkl.textbox_namebox_background}

    def _kkl_textbox_dialogue_properties():
        if not _kkl_textbox_template_active():
            return {}

        return {
            "font": _kkl_textbox_resolve_font(kkl.textbox_font),
            "color": kkl.textbox_text_color,
            "outlines": kkl.textbox_text_outlines,
        }

    def _kkl_textbox_name_properties():
        if not _kkl_textbox_template_active():
            return {}

        return {
            "font": _kkl_textbox_resolve_font(kkl.textbox_name_font),
            "color": kkl.textbox_name_color,
            "outlines": kkl.textbox_name_outlines,
        }


# 使用 style 语句而不是一次性修改，以便 Ren'Py 在 gui.rebuild() 后
#（包括语言切换后）重新应用模板。
init 110:

    style window:
        properties _kkl_textbox_window_properties()

    style namebox:
        properties _kkl_textbox_namebox_properties()

    style say_dialogue:
        properties _kkl_textbox_dialogue_properties()

    style say_thought:
        properties _kkl_textbox_dialogue_properties()

    style say_label:
        properties _kkl_textbox_name_properties()
