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
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import config

from data import Dataset

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.MINTY],
           )
data = Dataset('assets')


# ==================================== Helper functions =====================================


def _make_ssins_layout():
    return go.Layout(
        title=dict(
            text=f"SSINS Background-Subtracted Time-Series Avg. Across DTV7 (Night of {data.night}, pointing {data.pointing})",
            x=0.5, xanchor="center", font=dict(size=18)
        ),
        xaxis=dict(title="Time Step", type="linear", range=[-5, len(data.ssins)+5]),
        yaxis=dict(title="Amplitude Across DTV-7", type="linear"),
        font=dict(size=14),
        autosize=True,
        margin=dict(l=10, r=10, t=30, b=10),
        clickmode="event+select",
    )

def _make_annotations_layout():
    return go.Layout(
        title=dict(text="Annotations", x=0.5, xanchor="center", font=dict(size=18)),
        xaxis=dict(title="Time Step", type="linear", range=[-5, len(data.ssins)+5]),
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

def get_good(d):
    if d.good:
        return "Reject Dataset", "danger"
    else:
        return "Accept Dataset", "info"


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
                    html.H6(
                        f"Data source: {data._path}"
                    ),
                    width="auto"
                ),
                dbc.Col(
                    html.H6(
                        f"Total number of files: {data.get_n()}",
                        id="h6-n-files",
                    ),
                    width="auto"
                ),
                dbc.Col(
                    html.H6(
                        f"Number of annotated files: {data.count_annotations()}",
                        id="h6-count-annotations",
                    ),
                    width="auto"
                ),
                dbc.Col(
                    html.H6(
                        f"Number of bad files: {data.count_bad()}",
                        id="h6-count-bad",
                    ),
                    width="auto"
                )
            ],
            className="mt-0",
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
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
                        ),
                        dbc.Button(
                            "Set All Clean",
                            id="button-set-all-clean",
                            outline=False,
                            color="primary",
                            className="me-1",
                        ),
                    ],
                    width="auto",
                    className="mb-2",
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
                    [
                    dbc.Button(
                        "Export Annotations",
                        id="button-export",
                        color="primary",
                        style={"marginRight": "5px"}
                        ),
                    dbc.Button(
                        get_good(data)[0],
                        id="button-bad",
                        color=get_good(data)[1],
                        style={"marginLeft": "5px"}
                        ),
                    ],
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


# ======================================= Server Setup =================================

server = app.server

# ======================================= Callback functions ===========================


@app.callback(
    Output("annotation-graph", "figure", allow_duplicate=True),
    Input("button-set-1", "n_clicks"),
    Input("button-set-2", "n_clicks"),
    Input("button-set-3", "n_clicks"),
    Input("button-set-4", "n_clicks"),
    Input("button-set-all-clean", "n_clicks"),
    State("ssins-graph", "selectedData"),
    prevent_initial_call=True,
)
def set_state(b1,b2,b3,b4,ball, selectedData):

    try:
        points = selectedData["points"]
        x_selected = [p["x"] for p in points]
    except TypeError:
        x_selected = None

    triggered = ctx.triggered_id
    if triggered == "button-set-1":
        state_val = 1
    elif triggered == "button-set-2":
        state_val = 2
    elif triggered == "button-set-3":
        state_val = 3
    elif triggered == "button-set-4":
        state_val = 4
    elif triggered == "button-set-all-clean":
        state_val = 1
        x_selected = range(len(data.ssins))
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
    Output("button-bad", "children"),
    Output("button-bad", "color"),
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
        return no_update, no_update, prev_disabled, next_disabled, no_update, no_update

    # edge guards: do nothing if already at an endpoint
    if trigger == "button-prev" and cur_idx == 0:
        return no_update, no_update, True, next_disabled, \
                get_good(data)[0], get_good(data)[1]
    if trigger == "button-next" and cur_idx == max_idx:
        return no_update, no_update, prev_disabled, True, \
                get_good(data)[0], get_good(data)[1]

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

    return ssins_fig, ann_fig, new_prev_disabled, new_next_disabled, \
            get_good(data)[0], get_good(data)[1]



@app.callback(
    Output("ssins-graph", "figure", allow_duplicate=True),
    Output("annotation-graph", "figure", allow_duplicate=True),
    Output("button-p-all", "active"),
    Output("button-p-0", "active"),
    Output("button-p-1", "active"),
    Output("button-p-2", "active"),
    Output("button-p-3", "active"),
    Output("button-p-4", "active"),
    Output("button-bad", "children", allow_duplicate=True),
    Output("button-bad", "color", allow_duplicate=True),
    Output("h6-count-bad", "children", allow_duplicate=True),
    Output("h6-n-files", "children"),
    Output("h6-count-annotations", "children"),
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

    return ssins_fig, ann_fig, active[0], active[1], active[2], active[3], active[4], active[5], \
            get_good(data)[0], get_good(data)[1], f"Number of bad files: {data.count_bad()}", \
            f"Total number of files: {data.get_n()}", f"Number of annotated files: {data.count_annotations(p)}"


@app.callback(
    Output("save-toast", "is_open"),
    Output("save-toast", "children"),
    Output("h6-count-annotations", "children", allow_duplicate=True),
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
        return True, msg, no_update

    # Otherwise save
    annotations_path = data.save_annotations()
    return True, f"Annotations successfully saved in {annotations_path}", \
            f"Number of annotated files: {data.count_annotations(data.pointing_group)}"


@app.callback(
    Output("button-bad", "children", allow_duplicate=True),
    Output("button-bad", "color", allow_duplicate=True),
    Output("h6-count-bad", "children", allow_duplicate=True),
    Input("button-bad", "n_clicks"),
    prevent_initial_call=True,
)
def reject_accept(nbad):

    triggered = ctx.triggered_id
    if triggered == "button-bad":
        if data.good:
            data.mark_bad()
        else:
            data.mark_good()

    return get_good(data)[0], get_good(data)[1], f"Number of bad files: {data.count_bad()}"


if __name__ == "__main__":
    # app.run(debug=True, 
    #         host=config.BIND_ADDR, 
    #         port=config.BIND_PORT,
    #         dev_tools_hot_reload=False,
    #         )

    app.run_server(debug=True)
