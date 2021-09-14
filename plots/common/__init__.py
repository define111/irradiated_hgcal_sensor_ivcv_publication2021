# coding: utf-8

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch()

default_canvas_width = 1200
default_canvas_height = 900

default_style_props = {
  "Palette": 1,
  "PadTickX": 1,
  "PadTickY": 1,
  "TitleFont": 42,
  "StatFont": 42,

  "FrameFillColor": ROOT.kWhite,
  "FrameLineWidth": 1,
  "CanvasColor": ROOT.kWhite,
  "OptStat": 0,
  "LegendBorderSize": 0,
  "OptTitle": 0,

  "PadTopMargin": 0.05,
  "PadBottomMargin": 0.1,
  "PadLeftMargin": 0.12,
  "PadRightMargin": 0.05,

  "LegendTextSize": 0.80
}

default_canvas_props = {

}

default_pad_props = {

}

default_axis_props = {

}

default_auto_ticklength = 0.015

default_label_props = {
    "TextFont": 43,
    "TextSize": 32
}

default_legend_props = {
    "BorderSize": 0,
    "FillColor": 0,
    "LineStyle": 0,
    "LineColor": 0,
    "LineWidth": 0,
    "TextFont": 43,
    "TextSize": 32,
    "ColumnSeparation": 0.
}

default_hist_props = {

}

default_graph_props = {
    "MarkerSize": 3,
    "LineWidth": 4
}

default_line_props = {

}

default_box_props = {

}

default_func_props = {

}

colors = {
    "black": ROOT.kBlack,
    "blue": ROOT.kBlue + 1,
    "red": ROOT.kRed - 4,
    "magenta": ROOT.kMagenta + 1,
    "yellow": ROOT.kOrange - 2,
    "green": ROOT.kGreen + 2,
    "brightgreen": ROOT.kGreen - 3,
    "darkgreen": ROOT.kGreen + 4,
    "creamblue": 38,
    "creamred": 46,
    "white": 10
}



def setup_style(props=None):
    ROOT.gROOT.SetStyle("Plain")
    apply_root_properties(ROOT.gStyle, default_style_props, props)

    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetTitleSize(0.05, "xyz")

    ROOT.gROOT.ForceStyle()


def setup_canvas(canvas, width, height, props=None):
    canvas.SetWindowSize(width, height)
    canvas.SetCanvasSize(width, height)
    apply_root_properties(canvas, default_canvas_props, props)


def setup_pad(pad, props=None):
    apply_root_properties(pad, default_pad_props, props)


def setup_x_axis(x_axis, pad, props=None):
    _props = default_axis_props.copy()
    _props["TitleOffset"] = x_axis.GetTitleOffset()*0.93
    apply_root_properties(x_axis, _props, props)


def setup_y_axis(y_axis, pad, props=None):
    _props = default_axis_props.copy()
    apply_root_properties(y_axis, _props, props)


def setup_z_axis(z_axis, pad, props=None):
    _props = default_axis_props.copy()
    apply_root_properties(z_axis, _props, props)


def setup_label(label, props=None):
    apply_root_properties(label, default_label_props, props)


def calc_legend_pos(n_entries, x1=0.68, x2=0.96, y2=0.92, y_spread=0.05):
    y1 = y2 - y_spread * n_entries
    return (x1, y1, x2, y2)


def setup_legend(legend, props=None):
    apply_root_properties(legend, default_legend_props, props)


def get_canvas_pads(canvas):
    return [
        p for p in canvas.GetListOfPrimitives()
        if isinstance(p, ROOT.TPad)
    ]


def setup_hist(hist, props=None):
    apply_root_properties(hist, default_hist_props, props)


def setup_graph(graph, props=None):
    apply_root_properties(graph, default_graph_props, props)


def setup_line(line, props=None):
    apply_root_properties(line, default_line_props, props)


def setup_box(box, props=None):
    apply_root_properties(box, default_box_props, props)


def setup_func(func, props=None):
    apply_root_properties(func, default_func_props, props)


def update_canvas(canvas):
    for pad in get_canvas_pads(canvas):
        pad.RedrawAxis()
    ROOT.gPad.RedrawAxis()

    canvas.Update()


def apply_root_properties(obj, props, *_props):
    props = props.copy()
    for p in _props:
        if p:
            props.update(p)

    for name, value in props.items():
        setter = getattr(obj, "Set%s" % name, getattr(obj, name, None))
        if not hasattr(setter, "__call__"):
            continue

        if isinstance(value, tuple):
            # value might be a tuple (or list) of (class name, ...)
            # in that case, pass ROOT.<className>(*value[1:]) to the setter
            if isinstance(value[0], str):
                parts = value[0].split(".")
                cls = ROOT
                while parts:
                    part = parts.pop(0)
                    if not hasattr(cls, part):
                        cls = None
                        break
                    else:
                        cls = getattr(cls, part)
                if cls is not None:
                    setter(cls(*value[1:]))
                    continue

            setter(*value)
        else:
            setter(value)


def create_cms_labels(postfix="preliminary", x=0.135, y=0.96):
    label = ROOT.TLatex(x, y, "#font[22]{CMS HGCAL} " + postfix)
    setup_label(label)
    return label


def create_campaign_label(text="2020/21 irradiation at RINSC + annealing", x=0.93, y=0.96):
    label = ROOT.TLatex(x, y, text)
    setup_label(label, {"TextAlign": 31})
    return label