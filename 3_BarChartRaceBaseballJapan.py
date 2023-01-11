import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import matplotlib.cm as cm
import random
from tqdm import tqdm
import shutil

df_c = pd.read_csv('c_data.csv')
df_p = pd.read_csv('p_data.csv')

season = df_c['season'].drop_duplicates().tolist()


title = 'プロ野球 順位グラフ'
title_fontsize = 10
footnote1 = 'Data Source: 「日本プロ野球記録」https://2689web.com/games.html'
footnote2 = 'Source Code: https://github.com/Simple-Charts/BarChartRaceBaseballJapan'
footnote_fontsize = 6
xlabel_text = '勝率'
xlabel_fontsize = 7
tick_fontsize = 5
fontname = "Meiryo"
time_fontsize = 20
frames = 5
ranks = 8
image_dpi = 1000
video_height = 1000
video_width = 1600
video_fps = 60

def preprocess(df):
    df = df.fillna(0)
    df.index = df.index * frames
    df_value = df.reindex(range((len(df)-1)*frames+1))
    df_value['date'] = df_value['date'].fillna(method='ffill')
    df_value = df_value.set_index('date')
    df_rank = df_value.rank(axis=1, method='first')
    df_value = df_value.interpolate()
    for i in range(len(df_value)):
        zero_value = df_value.iloc[i].index[df_value.iloc[i] == 0.0]
        df_rank.iloc[i][zero_value] = 0
    df_rank = df_rank.interpolate()
    labels = df_value.columns
    colors = [cm.tab20(i / len(labels)) for i in range(ranks)]
    colors = [(color[0], color[1], color[2], 0.75) for color in colors]
    random.seed(0)
    random.shuffle(colors)
    return df_value, df_rank, labels, colors

def add_barh(ax, y, width, labels, colors):
    ax.barh(y = y, width = width, color = colors, tick_label = labels)
    ax.set_xlabel(xlabel_text, fontsize = xlabel_fontsize)
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', labelsize = tick_fontsize)
    ax.tick_params(axis='y', labelsize = tick_fontsize) 
    #for ticklabel, tickcolor in zip(ax.get_yticklabels(), colors):
    #    ticklabel.set_color(tickcolor)
    #ax.set_yticklabels([])
    ax.axes.yaxis.set_visible(False)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    [spine.set_visible(False) for spine in ax.spines.values()]
    ax.set_ylim(len(labels) - (ranks - 0.5), len(labels) + 0.5)
    ax.set_xlim(0,)
    for i, (value, lank, name) in enumerate(zip(width, y, labels)):
        if value != 0:
            ax.text(value+0.01, lank-0.25, name, ha='left')


for s in season:
    if os.path.exists("image"):
        shutil.rmtree("image")
    if not os.path.exists("image"):
        os.mkdir("image")

    df_c_temp = df_c.loc[df_c['season']==s,:].drop('season', axis=1)
    df_c_temp = df_c_temp.loc[:, (df_c_temp.sum(axis=0) != 0)]
    df_p_temp = df_p.loc[df_p['season']==s,:].drop('season', axis=1)
    df_p_temp = df_p_temp.loc[:, (df_p_temp.sum(axis=0) != 0)]

    df_c_temp = df_c_temp.reset_index(drop=True)
    df_p_temp = df_p_temp.reset_index(drop=True)

    c_value, c_rank, c_labels, c_colors = preprocess(df_c_temp)
    p_value, p_rank, p_labels, p_colors = preprocess(df_p_temp)

    for i in tqdm(range(len(c_value))):
        fig = plt.figure()
        plt.rcParams["font.family"] = fontname

        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)

        add_barh(ax1, y = c_rank.iloc[i], width = c_value.iloc[i], labels = c_labels, colors = c_colors)
        add_barh(ax2, y = p_rank.iloc[i], width = p_value.iloc[i], labels = p_labels, colors = p_colors)

        plt.tight_layout()
        plt.suptitle(title, y=0.95, fontsize = title_fontsize)
        plt.subplots_adjust(left=0.05, right=0.70, bottom=0.1, top=0.8, hspace=0.3)
        plt.text(0.98, 0.9, c_value.index[i][0:10], transform = fig.transFigure, size = time_fontsize, ha='right', weight=750)

        plt.text(0.02, 0.01, footnote1, transform = fig.transFigure, size = footnote_fontsize, ha='left')
        plt.text(0.02, 0.03, footnote2, transform = fig.transFigure, size = footnote_fontsize, ha='left')
        
        plt.text(0.02, 0.85, "セリーグ", transform = fig.transFigure, size = 9, ha='left')
        plt.text(0.02, 0.45, "パリーグ", transform = fig.transFigure, size = 9, ha='left')
        
        plt.savefig("image/img"+str(i).zfill(4)+".png", dpi=image_dpi)
        plt.clf()
        plt.close()
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video = cv2.VideoWriter(str(s) + '.mp4', fourcc, fps = video_fps, frameSize = (video_width, video_height))
    for i in tqdm(range(len(c_value))):
        img = cv2.imread('image/img%04d.png' % i)
        img = cv2.resize(img, (video_width, video_height))
        video.write(img)
    video.release()