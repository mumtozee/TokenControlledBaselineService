import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

model_path = "./data/controlled_generation/models/baseline"
model = AutoModelForCausalLM.from_pretrained(model_path)
toker = AutoTokenizer.from_pretrained(f"{model_path}/tokenizer")

model.to(DEVICE)
model.eval()

MAX_LEN = 500


def get_first_sentence(text: str):
    splitted = text.split('.')
    answer = splitted[0]
    if len(splitted) >= 2 and len(splitted[1]) > 0:
        answer = " ".join([answer, ".", splitted[1]])
    answer = answer.strip()
    if answer[len(answer) - 1] != '?' and answer[len(answer) - 1] != '!':
        answer = "".join([answer, "."])
    return answer


def gen_response(text):
    input_ids = toker.encode(text, return_tensors='pt')
    hist_len = input_ids.shape[1]
    if hist_len > MAX_LEN:
        input_ids = input_ids[:, hist_len - MAX_LEN:hist_len]
    response_ids = model.generate(
        input_ids.to(DEVICE),
        max_length=500,
        pad_token_id=toker.pad_token_id,
        top_p=0.92,
        top_k=51
    )
    response = toker.decode(
        response_ids[:, input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )
    return get_first_sentence(response.strip())


def gen_response_batch(text_batch):
    input_ids = toker(text_batch, return_tensors='pt',
                      padding=True)["input_ids"]
    response_ids = model.generate(
        input_ids.to(DEVICE),
        max_length=500,
        pad_token_id=toker.pad_token_id,
        top_p=0.92,
        top_k=50
    )
    response = toker.batch_decode(
        response_ids[:, input_ids.shape[-1]:],
        skip_special_tokens=True
    )

    for i in range(len(response)):
        response[i] = get_first_sentence(response[i].strip())
    return response
