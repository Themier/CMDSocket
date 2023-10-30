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
from  ..coreCommands import CommandBase
from tools import ChoiceBox
from config import ConfigIOer

makeGif_id = '*makeGif'
makeGif_abbr = '*mg'

latestSourcePathsId = 'cmdArg_*makeGif_latestSourcePaths'
latestNumsId = 'cmdArg_*makeGif_latestNums'
latestBeginAtId = 'cmdArg_*makeGif_latestBeginAt'
latestIntersId = 'cmdArg_*makeGif_latestInters'
latestPrefixesId = 'cmdArg_*makeGif_latestPrefixes'
latestSuffixesId = 'cmdArg_*makeGif_latestSuffixes'
latestGifNameId = 'cmdArg_*makeGif_latestGifName'
latestFrameDurationId = 'cmdArg_*makeGif_latestFrameDuration'

defaultGifName = 'default.gif'
defaultFrameDuration = 0.1


def makeGif(cmd, customAddr, link:socket.socket):
    source_paths = cmd.get('source_paths')
    nums = cmd.get('nums')
    begin_at = cmd.get('begin_at')
    inters = cmd.get('inters')
    prefixes = cmd.get('prefixes')
    suffixes = cmd.get('suffixes')
    gif_name = cmd.get('gif_name')
    gif_path = os.path.join(source_paths[0], gif_name)
    frame_duration = cmd.get('frame_duration')
    with imageio.get_writer(gif_path, mode='I', duration=frame_duration) as writer:
        for source_path, num, begin, inter, prefix, suffix in zip(source_paths, nums, begin_at, inters, prefixes, suffixes):
            print(f'reading path {source_path}')
            for index in tqdm(range(begin, begin + num, inter), 'writing gif'):
                file_path = os.path.join(source_path, '{}{:04d}{}'.format(prefix, index, suffix))
                image = imageio.imread(file_path)
                writer.append_data(image)
    
    return


def genMakeGif(d:dict={}):
    global defaultGifName, defaultFrameDuration
    global latestSourcePathsId, latestNumsId, latestBeginAtId, latestIntersId
    global latestPrefixesId, latestSuffixesId, latestGifNameId, latestFrameDurationId
    source_paths = d.get('source_paths', ConfigIOer.getSTDConfig(latestSourcePathsId, []))
    nums = d.get('nums', ConfigIOer.getSTDConfig(latestNumsId, []))
    begin_at = d.get('begin_at', ConfigIOer.getSTDConfig(latestBeginAtId, []))
    inters = d.get('inters', ConfigIOer.getSTDConfig(latestIntersId, []))
    prefixes = d.get('prefixes', ConfigIOer.getSTDConfig(latestPrefixesId, []))
    suffixes = d.get('suffixes', ConfigIOer.getSTDConfig(latestSuffixesId, []))
    gif_name = d.get('gif_path', ConfigIOer.getSTDConfig(latestGifNameId, defaultGifName))
    frame_duration = d.get('frame_duration', float(ConfigIOer.getSTDConfig(latestFrameDurationId, defaultFrameDuration)))
    while True:
        print('资源路径: {}\n资源数量: {}\n帧序起始: {}\n帧间距: {}\n资源名前缀: {}\n资源名后缀: {}\ngif命名: {}\n单帧时长: {}'
              .format(source_paths, nums, begin_at, inters, prefixes, suffixes, gif_name, frame_duration))
        cb = ChoiceBox()
        cb.newChoice('添加资源路径')
        cb.newChoice('移除资源路径')
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
        if inp == '移除资源路径':
            removeCb = ChoiceBox()
            for path in source_paths:
                removeCb.newChoice(path)
            while True:
                which = removeCb.getChoice('移除哪一个？', addConfirm=False)
                if which in source_paths:
                    index = source_paths.index(which)
                    source_paths.pop(index)
                    nums.pop(index)
                    begin_at.pop(index)
                    inters.pop(index)
                    prefixes.pop(index)
                    suffixes.pop(index)
                    break
                elif which == ChoiceBox.cancelId:
                    break
        elif inp == '重命名 gif':
            gif_name = input('重命名: ')
        elif inp == '改变单帧时长':
            frame_duration = input('单帧时长: ')
        elif inp == ChoiceBox.confirmId:
            cmd = {}
            cmd.update({'cmdId': makeGif_id, 'source_paths':source_paths, 'nums':nums \
                        , 'begin_at':begin_at, 'inters':inters, 'prefixes':prefixes \
                        , 'suffixes':suffixes, 'gif_name':gif_name, 'frame_duration':frame_duration})
            ConfigIOer.writeSTDConfig(latestSourcePathsId, source_paths)
            ConfigIOer.writeSTDConfig(latestNumsId, nums)
            ConfigIOer.writeSTDConfig(latestBeginAtId, begin_at)
            ConfigIOer.writeSTDConfig(latestIntersId, inters)
            ConfigIOer.writeSTDConfig(latestPrefixesId, prefixes)
            ConfigIOer.writeSTDConfig(latestSuffixesId, suffixes)
            ConfigIOer.writeSTDConfig(latestGifNameId, gif_name)
            ConfigIOer.writeSTDConfig(latestFrameDurationId, frame_duration)
            return cmd
        elif inp == ChoiceBox.cancelId:
            return None


CommandBase(makeGif_id, makeGif, genMakeGif, abbr=makeGif_abbr)
