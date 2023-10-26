from typing import List
import os, socket
import imageio
from tqdm import tqdm
from commands import CommandBase
from tools import ChoiceBox

makeGif_id = '*makeGif'
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
        print('source path: {}\nnums: {}\nbegin_at: {}\ninters: {}\nprefixes: {}\nsuffixes: {}\ngif_name: {}\nframe_duration: {}'
              .format(source_paths, nums, begin_at, inters, prefixes, suffixes, gif_name, frame_duration))
        cb = ChoiceBox()
        cb.newChoice('add source')
        cb.newChoice('rename gif')
        cb.newChoice('change frame duration')
        inp = cb.getChoice('make gif ?')
        if inp == 'add source':
            source_paths.append(input('new source path: '))
            nums.append(int(input('frame num: ')))
            begin_at.append(int(input('frame begin at: ')))
            inters.append(int(input('frame index inters: ')))
            prefixes.append(input('prefix: '))
            suffixes.append(input('suffix: '))
        elif inp == 'rename gif':
            gif_name = input('new name: ')
        elif inp == 'change frame duration':
            frame_duration = input('new frame duration: ')
        elif inp == ChoiceBox.confirmId:
            cmd = {}
            cmd.update({'cmdId': makeGif_id, 'source_paths':source_paths, 'nums':nums \
                        , 'begin_at':begin_at, 'inters':inters, 'prefixes':prefixes \
                        , 'suffixes':suffixes, 'gif_name':gif_name, 'frame_duration':frame_duration})
            return cmd
        elif inp == ChoiceBox.cancelId:
            return None


CommandBase(makeGif_id, makeGif, genMakeGif)
