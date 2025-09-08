from dash import (
    Dash,
    html,
    dcc,
    callback,
    Output,
    Input,
    State,
    no_update,
    ctx,
    ALL,
)
import dash
import math
import numpy as np
import plotly.graph_objects as go
import plotly.colors as colors
import dash_bootstrap_components as dbc
import json
import config
import re

from data import Dataset

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.MINTY],
           )
data = Dataset('assets')


# ==================================== Helper functions =====================================


from dash import callback, Output, Input, no_update, ctx
import numpy as np
import plotly.graph_objects as go

def _make_ssins_layout():
    return go.Layout(
        title=dict(
            text=f"SSINS Background-Subtracted Time-Series (Night of {data.night}, pointing {data.pointing})",
            x=0.5, xanchor="center", font=dict(size=18)
        ),
        xaxis=dict(title="Frequency Step", type="linear", range=[-5, len(data.ssins)+5]),
        yaxis=dict(title="Amplitude Across DTV-7", type="linear"),
        font=dict(size=14),
        autosize=True,
        margin=dict(l=10, r=10, t=30, b=10),
        clickmode="event+select",
    )

def _make_annotations_layout():
    return go.Layout(
        title=dict(text="Annotations", x=0.5, xanchor="center", font=dict(size=18)),
        xaxis=dict(title="Frequency Step", type="linear", range=[-5, len(data.ssins)+5]),
        yaxis=dict(title="HMM State", type="linear", range=[0.5, 4.5], tickmode="array", tickvals=[1,2,3,4]),
        font=dict(size=14),
        autosize=True,
        margin=dict(l=10, r=10, t=30, b=10),
    )

def _build_ssins_figure():
    fig = go.Figure(layout=_make_ssins_layout())
    fig.add_trace(go.Scatter(
        x=np.arange(len(data.ssins)),
        y=data.ssins,
        mode="markers",
        marker=dict(size=6, color="blue"),
    ))
    return fig

def _build_annotations_figure():
    fig = go.Figure(layout=_make_annotations_layout())
    fig.add_trace(go.Scatter(
        x=np.arange(len(data.annotations)),
        y=data.annotations,
        mode="lines",
        line=dict(color="red", width=4),
    ))
    return fig


# ==================================== App Layout =====================================


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1(
                    "HMM Annotator",
                    className="text-center mt-2",
                ),
            ],
            className="mt-0",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Set State 1 (Clean)",
                                id="button-set-1",
                                outline=False,
                                color="primary",
                                className="me-1",
                            ),
                            dbc.Button(
                                "Set State 2 (RFI-Rising)",
                                id="button-set-2",
                                outline=False,
                                color="primary",
                                className="me-1",
                            ),
                            dbc.Button(
                                "Set State 3 (RFI-Decaying)",
                                id="button-set-3",
                                outline=False,
                                color="primary",
                                className="me-1",
                            ),
                            dbc.Button(
                                "Set State 4 (Blip)",
                                id="button-set-4",
                                outline=False,
                                color="primary",
                                className="me-1",
                            ),
                        ],
                        className="mb-2",
                    ),
                    width="auto",
                ),
            ],
            className="mt-2 mb-2",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "< Previous Night",
                        id="button-prev",
                        color="secondary"
                        ),
                    width=4,
                    className="text-start"
                ),
                dbc.Col(
                    dbc.Button(
                        "Export Annotations",
                        id="button-export",
                        color="secondary"
                        ),
                    width=4,
                    className="text-center"
                ),
                dbc.Col(
                    dbc.Button(
                        "Next Night >",
                        id="button-next",
                        color="secondary"
                        ),
                    width=4,
                    className="text-end"
                )
            ],
            className="mb-4",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="ssins-graph",
                        figure=_build_ssins_figure(),
                        style={"display": "inline-block", "height": "35vh", "width":"100%"},
                    ),
                    width=12,
                    className="mb-0 mt-o",
                ),
            ],
            className="mt-0",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="annotation-graph",
                        figure=_build_annotations_figure(),
                        style={"display": "inline-block", "height": "35vh", "width": "100%"},
                    ),
                    width=12,
                    className="mb-0 mt-o",
                ),
            ],
            className="mt-0",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "All pointings",
                                id="button-p-all",
                                outline=False,
                                color="primary",
                                className="me-1",
                                active=True,
                            ),
                            dbc.Button(
                                "Pointing 0",
                                id="button-p-0",
                                outline=False,
                                color="primary",
                                className="me-1",
                                active=False,
                            ),
                            dbc.Button(
                                "Pointing 1",
                                id="button-p-1",
                                outline=False,
                                color="primary",
                                className="me-1",
                                active=False,
                            ),
                            dbc.Button(
                                "Pointing 2",
                                id="button-p-2",
                                outline=False,
                                color="primary",
                                className="me-1",
                                active=False,
                            ),
                            dbc.Button(
                                "Pointing 3",
                                id="button-p-3",
                                outline=False,
                                color="primary",
                                className="me-1",
                                active=False,
                            ),
                            dbc.Button(
                                "Pointing 4",
                                id="button-p-4",
                                outline=False,
                                color="primary",
                                className="me-1",
                                active=False,
                            ),
                        ],
                    ),
                    width="auto",
                )
            ],
            className="mt-0",
            justify="center",
            align="center",
        ),
        dbc.Toast(
            children="Flags successfully saved!",
            id="save-toast",
            header="Notification",
            icon="success",
            duration=4000,
            is_open=False,
            dismissable=True,
            style={"position": "fixed", "top": 10, "right": 10, "width": 350},
        ),
    ]
)


# ======================================= Callback functions ===========================


@app.callback(
    Output("annotation-graph", "figure", allow_duplicate=True),
    Input("button-set-1", "n_clicks"),
    Input("button-set-2", "n_clicks"),
    Input("button-set-3", "n_clicks"),
    Input("button-set-4", "n_clicks"),
    State("ssins-graph", "selectedData"),
    prevent_initial_call=True,
)
def set_state(b1,b2,b3,b4, selectedData):

    points = selectedData["points"]
    x_selected = [p["x"] for p in points]

    triggered = ctx.triggered_id
    if triggered == "button-set-1":
        state_val = 1
    elif triggered == "button-set-2":
        state_val = 2
    elif triggered == "button-set-3":
        state_val = 3
    elif triggered == "button-set-4":
        state_val = 4
    else:
        state_val = None

    if state_val is not None:
        data.annotations[x_selected] = state_val

    # Rebuild annotation graph
    fig = go.Figure(layout=_make_annotations_layout())
    fig.add_trace(
        go.Scatter(
            x=np.arange(len(data.annotations)),
            y=data.annotations,
            mode="lines",
            line=dict(color="red", width=4),
            name="Annotations",
        )
    )

    return fig


@callback(
    Output("ssins-graph", "figure"),
    Output("annotation-graph", "figure"),
    Output("button-prev", "disabled"),
    Output("button-next", "disabled"),
    Input("button-prev", "n_clicks"),
    Input("button-next", "n_clicks"),
    prevent_initial_call=False,
)
def change_night(prev_clicks, next_clicks):

    try:
        cur_idx = data.filenames.index(data.filename)
    except Exception:
        cur_idx = 0
    max_idx = len(data.filenames) - 1

    # disabled states for current position
    prev_disabled = (cur_idx == 0)
    next_disabled = (cur_idx == max_idx)

    # on first load (no trigger), just set disabled states
    trigger = ctx.triggered_id
    if not trigger:
        return no_update, no_update, prev_disabled, next_disabled

    # edge guards: do nothing if already at an endpoint
    if trigger == "button-prev" and cur_idx == 0:
        return no_update, no_update, True, next_disabled
    if trigger == "button-next" and cur_idx == max_idx:
        return no_update, no_update, prev_disabled, True

    direction = -1 if trigger == "button-prev" else +1
    new_idx = cur_idx + direction
    new_name = data.filenames[new_idx]

    data.set_filename(new_name)

    # recompute disabled states at new position
    new_prev_disabled = (new_idx == 0)
    new_next_disabled = (new_idx == max_idx)

    # rebuild figures for the new night
    ssins_fig = _build_ssins_figure()
    ann_fig = _build_annotations_figure()

    return ssins_fig, ann_fig, new_prev_disabled, new_next_disabled



@app.callback(
    Output("ssins-graph", "figure", allow_duplicate=True),
    Output("annotation-graph", "figure", allow_duplicate=True),
    Output("button-p-all", "active"),
    Output("button-p-0", "active"),
    Output("button-p-1", "active"),
    Output("button-p-2", "active"),
    Output("button-p-3", "active"),
    Output("button-p-4", "active"),
    Input("button-p-all", "n_clicks"),
    Input("button-p-0", "n_clicks"),
    Input("button-p-1", "n_clicks"),
    Input("button-p-2", "n_clicks"),
    Input("button-p-3", "n_clicks"),
    Input("button-p-4", "n_clicks"),
    prevent_initial_call=True,
)
def switch_pointing(pall,p0,p1,p2,p3,p4):
    triggered = ctx.triggered_id

    active = [False,False,False,False,False,False]

    if triggered == "button-p-all":
        p = 'p'
        active[0] = True
    elif triggered == "button-p-0":
        p = 'p0'
        active[1] = True
    elif triggered == "button-p-1":
        p = 'p1'
        active[2] = True
    elif triggered == "button-p-2":
        p = 'p2'
        active[3] = True
    elif triggered == "button-p-3":
        p = 'p3'
        active[4] = True
    elif triggered == "button-p-4":
        p = 'p4'
        active[5] = True

    data.set_pointing(p)

    # rebuild figures for the new pointing
    ssins_fig = _build_ssins_figure()
    ann_fig = _build_annotations_figure()

    return ssins_fig, ann_fig, active[0], active[1], active[2], active[3], active[4], active[5], 





@app.callback(
    Output("save-toast", "is_open"),
    Output("save-toast", "children"),
    Input("button-export", "n_clicks"),
    prevent_initial_call=True,
)
def export(n):
    if not n:
        return no_update, no_update

    # Block export if any unannotated points (zeros) remain
    missing = int(np.count_nonzero(data.annotations == 0))
    if missing > 0:
        msg = f"Export blocked: {missing} unannotated point(s) remain. Label all points (1, 2, or 3) before exporting."
        return True, msg

    # Otherwise save
    annotations_path = data.save_annotations()
    return True, f"Annotations successfully saved in {annotations_path}"



if __name__ == "__main__":
    app.run(debug=True, 
            host=config.BIND_ADDR, 
            port=config.BIND_PORT,
            dev_tools_hot_reload=False,
            )
