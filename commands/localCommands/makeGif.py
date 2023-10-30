from typing import List
import os, socket
try:
    import imageio
except Exception as error:
    print(error)
try:
    from tqdm import tqdm
except Exception as error:
    print(error)
from commands import CommandBase
from tools import ChoiceBox

makeGif_id = '*makeGif'
makeGif_abbr = '*mg'
makeGif_latestSourcePaths = []
makeGif_latestNums = []
makeGif_latestBeginAt = []
makeGif_latestInters = []
makeGif_latestPrefixes = []
makeGif_latestSuffixes = []
makeGif_defaultGifPath = './default.gif'
makeGif_latestGifPath = makeGif_defaultGifPath
makeGif_defaultFrameDuration = 0.1
makeGif_latestFrameDuration = makeGif_defaultFrameDuration

def makeGif(cmd, customAddr, link:socket.socket):
    global makeGif_defaultGifPath, makeGif_defaultFrameDuration
    source_paths = cmd.get('source_paths', [])
    nums = cmd.get('nums', [])
    begin_at = cmd.get('begin_at', [])
    inters = cmd.get('inters', [])
    prefixes = cmd.get('prefixes', [])
    suffixes = cmd.get('suffixes', [])
    gif_name = cmd.get('gif_name', makeGif_defaultGifPath)
    gif_path = os.path.join(source_paths[0], gif_name)
    frame_duration = cmd.get('frame_duration', makeGif_defaultFrameDuration)
    with imageio.get_writer(gif_path, mode='I', duration=frame_duration) as writer:
        for source_path, num, begin, inter, prefix, suffix in zip(source_paths, nums, begin_at, inters, prefixes, suffixes):
            print(f'reading path {source_path}')
            for index in tqdm(range(begin, begin + num, inter), 'writing gif'):
                file_path = os.path.join(source_path, '{}{:04d}{}'.format(prefix, index, suffix))
                image = imageio.imread(file_path)
                writer.append_data(image)
    
    return


def genMakeGif(d:dict={}):
    source_paths = d.get('source_paths', makeGif_latestSourcePaths)
    nums = d.get('nums', makeGif_latestNums)
    begin_at = d.get('begin_at',makeGif_latestBeginAt)
    inters = d.get('inters', makeGif_latestInters)
    prefixes = d.get('prefixes', makeGif_latestPrefixes)
    suffixes = d.get('suffixes', makeGif_latestSuffixes)
    gif_name = d.get('gif_path', makeGif_defaultGifPath)
    frame_duration = d.get('frame_duration', makeGif_latestFrameDuration)
    while True:
        print('资源路径: {}\n资源数量: {}\n帧序起始: {}\n帧间距: {}\n资源名前缀: {}\n资源名后缀: {}\ngif命名: {}\n单帧时长: {}'
              .format(source_paths, nums, begin_at, inters, prefixes, suffixes, gif_name, frame_duration))
        cb = ChoiceBox()
        cb.newChoice('添加资源路径')
        cb.newChoice('重命名 gif')
        cb.newChoice('改变单帧时长')
        inp = cb.getChoice('合成 gif ?')
        if inp == '添加资源路径':
            source_paths.append(input('资源路径: '))
            nums.append(int(input('资源数量: ')))
            begin_at.append(int(input('帧序起始: ')))
            inters.append(int(input('帧间距: ')))
            prefixes.append(input('资源名前缀: '))
            suffixes.append(input('资源名后缀: '))
        elif inp == '重命名 gif':
            gif_name = input('重命名: ')
        elif inp == '改变单帧时长':
            frame_duration = input('单帧时长: ')
        elif inp == ChoiceBox.confirmId:
            cmd = {}
            cmd.update({'cmdId': makeGif_id, 'source_paths':source_paths, 'nums':nums \
                        , 'begin_at':begin_at, 'inters':inters, 'prefixes':prefixes \
                        , 'suffixes':suffixes, 'gif_name':gif_name, 'frame_duration':frame_duration})
            return cmd
        elif inp == ChoiceBox.cancelId:
            return None


CommandBase(makeGif_id, makeGif, genMakeGif, abbr=makeGif_abbr)
