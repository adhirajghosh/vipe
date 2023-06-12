import os

import torch
from transformers import BertTokenizer, BertForSequenceClassification, GPT2LMHeadModel, GPT2Tokenizer
from torch.utils.data import DataLoader
from datasets import load_dataset
from datasets import Dataset
from utils import visualizer, get_vis_batch, save_s_json, get_vis_flute_samples,update_dataset,get_haivment_prompts
import json
import random
# Load the dataset
dataset = load_dataset("ColumbiaNLP/FLUTE")

import random

# Set the random seed for reproducibility
seed = 42
random.seed(seed)




device='cuda'
os.environ['CUDA_VISIBLE_DEVICES']='0'
HAIVMet_Dir='/graphics/scratch2/staff/Hassan/datasets/HAIVMet/flute.zip'
vis_samples=get_vis_flute_samples(HAIVMet_Dir)

print(' found ', len(vis_samples), ' to be replaced in the dataset')
do_sample=False
use_visual_data=False # my data or haivmet data

Use_HAIVMet_prompts=False # set to false to use your generated prompt
shuffle=False


model_name='gpt2-medium'
checkpoint_name = '{}_context_ctx_7_lr_5e-05-v4'.format(model_name)
if Use_HAIVMet_prompts and use_visual_data:
    checkpoint_name='humans'
elif not use_visual_data and not Use_HAIVMet_prompts:
    checkpoint_name = 'textual'

saving_dir='/graphics/scratch2/staff/Hassan/checkpoints/lyrics_to_prompts/vis_emotion/Vis_FLUTE/vis_{}_shuffle_{}_haivmet_{}/{}/'.format(use_visual_data,shuffle,Use_HAIVMet_prompts,checkpoint_name)

# Create the directory if it does not exist
if not os.path.exists(saving_dir):
    os.makedirs(saving_dir)

os.makedirs(saving_dir + 'images/',exist_ok=True)
#checkpoint_name = 'gpt2-large_context_ctx_1_lr_5e-05-v3.ckpt'



from img_tools import generate_images

if use_visual_data and not Use_HAIVMet_prompts:
    print('loading the visual version of the data')
    with open(saving_dir + 'vis_flute_train_sample_{}_{}'.format(do_sample, checkpoint_name)) as file:
        vis_train = json.load(file)
    with open(saving_dir + 'vis_flute_valid_sample_{}_{}'.format(do_sample, checkpoint_name)) as file:
        vis_valid = json.load(file)

    print('generating train images')
    prompt_dict={i:p for i,p in zip(vis_train['ids'],vis_train['vis_text'])}
    generate_images(prompt_dict=prompt_dict,saving_path=saving_dir + 'images/',batch_size=5,gpu=0)

    print('generating valid images')
    prompt_dict = {i: p for i, p in zip(vis_valid['ids'], vis_valid['vis_text'])}
    generate_images(prompt_dict=prompt_dict, saving_path=saving_dir + 'images/', batch_size=5, gpu=0)


elif use_visual_data and Use_HAIVMet_prompts:

    # if generate_haivment_data:
    #     HAIVMet_Dir = '/graphics/scratch2/staff/Hassan/datasets/HAIVMet/flute.zip'
    #     vis_valid=get_haivment_prompts(HAIVMet_Dir,vis_samples,valid_dataset )
    #     vis_train = get_haivment_prompts(HAIVMet_Dir, vis_samples, train_dataset)

        # save_s_json(saving_dir, 'vis_flute_train_sample_{}_{}'.format(do_sample, checkpoint_name), vis_train)
        # save_s_json(saving_dir, 'vis_flute_valid_sample_{}_{}'.format(do_sample, checkpoint_name), vis_valid)

    with open(saving_dir + 'vis_flute_train_sample_{}_{}'.format(do_sample, checkpoint_name)) as file:
        vis_train = json.load(file)
    with open(saving_dir + 'vis_flute_valid_sample_{}_{}'.format(do_sample, checkpoint_name)) as file:
        vis_valid = json.load(file)

    print('generating train images')
    prompt_dict = {i: p for i, p in zip(vis_train['ids'], vis_train['vis_text'])}
    generate_images(prompt_dict=prompt_dict, saving_path=saving_dir + 'images/', batch_size=8, gpu=0)

    print('generating valid images')
    prompt_dict = {i: p for i, p in zip(vis_valid['ids'], vis_valid['vis_text'])}
    generate_images(prompt_dict=prompt_dict, saving_path=saving_dir + 'images/', batch_size=8, gpu=0)

else:

    all_samples=dataset['train']

    HAIVMet_Dir = '/graphics/scratch2/staff/Hassan/datasets/HAIVMet/flute.zip'
    vis_samples = get_vis_flute_samples(HAIVMet_Dir)

    #all_samples.filter(samle:)
    filtered_dataset = all_samples.filter(lambda example: example['hypothesis'] in vis_samples)

    prompt_dict={k:v for k,v in zip(filtered_dataset['id'],filtered_dataset['hypothesis'])}
    generate_images(prompt_dict=prompt_dict, saving_path=saving_dir + 'images/', batch_size=8, gpu=0)