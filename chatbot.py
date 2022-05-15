from ctypes import Union
from typing import Optional, Union, Any

from df_engine.core.keywords import TRANSITIONS, RESPONSE
from df_engine.core import Context, Actor

import df_engine.labels as lbl
import df_engine.conditions as cnd

import requests
import random
import re
import json

URL = "http://127.0.0.1:5500/respond"
ACTS = ["[DA_1]", "[DA_2]", "[DA_3]", "[DA_4]"]
EOS_TOKEN = "<|endoftext|>"


def get_response(ctx: Context, actor: Actor, *args, **kwargs) -> Any:
    response = ""
    history = ""
    indices = list(ctx.responses)
    for idx in indices:
        history = f"{EOS_TOKEN}".join(
            [history, ctx.requests[idx], ctx.responses[idx]])

    request = ctx.last_request
    history = f"{EOS_TOKEN}".join([history, request])
    act_idx = random.randint(0, len(ACTS) - 1)
    data = {
        "history": f"{history}{EOS_TOKEN}{ACTS[act_idx]}"
    }
    j_data = json.dumps(data)
    r = requests.post(URL, data=j_data)
    response = json.loads(r.text)["data"]
    return response


plot = {
    "global_flow": {
        "start_node": {
            RESPONSE: "Hello, say hi to start a conversation :)",
            TRANSITIONS: {
                ("main_flow", "node_1"): cnd.regexp(r"hi|hello|hey", re.I),
                ("fallback_node"): cnd.true()
            }
        },
        "fallback_node": {
            RESPONSE: "Ooops",
            TRANSITIONS: {
                ("main_flow", "node_1"): cnd.regexp(r"hi|hello|hey", re.I),
                lbl.previous(): cnd.regexp(r"prev", re.I),
                lbl.repeat(): cnd.true()
            }
        }
    },
    "main_flow": {
        "node_1": {
            RESPONSE: get_response,
            TRANSITIONS: {
                lbl.to_fallback(): cnd.exact_match("stop"),
                lbl.repeat(): cnd.true()
            }
        }
    }
}

actor = Actor(plot, start_label=("global_flow", "start_node"),
              fallback_label=("global_flow", "fallback_node"))


def turn_handler(
    in_request: str, ctx: Union[Context, str, dict], actor: Actor,
    true_out_response: Optional[str] = None
):
    ctx = Context.cast(ctx)
    ctx.add_request(in_request)
    ctx = actor(ctx)
    out_response = ctx.last_response
    return out_response, ctx


def run_interactive_mode(actor):
    ctx = {}
    while True:
        in_request = input("You: ")
        out_response, ctx = turn_handler(in_request, ctx, actor)
        print(f"Bot: {out_response}")


if __name__ == "__main__":
    run_interactive_mode(actor)
