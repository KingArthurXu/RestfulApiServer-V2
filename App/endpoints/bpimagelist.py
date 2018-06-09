#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import collections as coll
import shlex
import unittest

from configparser import ConfigParser
from flask_restplus import Resource, Namespace

ns_bpimagelist = Namespace('bpimagelist', __name__)


@ns_bpimagelist.route('/bp')
class Bpimagelist(Resource):

    # @auth_token_required
    @staticmethod
    def get():
        u"""
        测试解析bpimagelist文件中各字段
        使用配置文件 testdata下bpimagelist.ini
        ```
        [bpimagelist]
        filename = App / testdata / copilot_bpimagelist.txt
        ```
        读取测试用的bpimagelist文件，并尝试解析其中各字段
        """
        config = ConfigParser()
        config.read('App/testdata/bpimagelist.ini')
        bpimagelist_file = config['bpimagelist']['filename']
        bp_file = open(bpimagelist_file, "r")
        bp_lines = bp_file.readlines()
        bp_file.close()

        output_list = bpimagelist_analyze(bp_lines)
        return output_list


def bpimagelist_analyze(bp_lines=None):
    # 定义多Netbackup输出字段配置
    image_line_base_names = (
        'IMAGE ClientName Data1 Data2 Version '  # 1..5
        ' BackupID PolicyName Client_Type ProxyClient Creator '  # 6..10
        ' ScheduleLabel ScheduleType RetentionLevel BackupTime ElapsedTimeInSeconds'  # 11..15
        ' Expiration Compression Encryption KbyteWrittn NumberOfFiles'
        ' Copies NumberOfFragments FilesFileCompressed FilesFile SoftwareVersion'
        ' Name1 bpimagelistInputOptions PrimaryCopy ImageType TrueImageRecoveryInfo'
        ' TrueImageRecoveryExpiration Keywords MPX ExtendedSecurityInfo IndividualFileRestorefromRaw'
        ' ImageDumpLevel FileSystemOnly PreviousBlockIncrementalTime BlockIncrementalFullTime ObjectDescription'
        ' RequestID BackupStatus BackupCopy PrevBackupImage JobID'
        ' NumberofResumes ResumeExpiration FilesFileSize PFIType ImageAttribute'
    )

    imageline50 = coll.namedtuple('IMAGE54', image_line_base_names +
                                  ' DataClassificationID StorageLifecyclePolicy STL_Completed SnapTime')
    imageline54 = coll.namedtuple('IMAGE54', image_line_base_names +
                                  ' DataClassificationID StorageLifecyclePolicy STL_Completed SnapTime')
    imageline55 = coll.namedtuple('IMAGE55', image_line_base_names +
                                  ' DataClassificationID StorageLifecyclePolicy STL_Completed SnapTime SLPVersion')
    imageline58 = coll.namedtuple('IMAGE58', image_line_base_names +
                                  ' DataClassificationID StorageLifecyclePolicy STL_Completed SnapTime SLPVersion'
                                  ' RemoteExpiration OriginMasterServer OriginMasterGUID')
    imageline62 = coll.namedtuple('IMAGE62', image_line_base_names +
                                  ' DataClassificationID StorageLifecyclePolicy STL_Completed SnapTime SLPVersion'
                                  ' RemoteExpiration OriginMasterServer OriginMasterGUID IREnabled ClientCharacterSet'
                                  ' ImageonHold IndexingStatus')
    image_line_dict = {
        50: imageline50,
        54: imageline54,
        55: imageline55,
        58: imageline58,
        62: imageline62, }

    frag_line_base_name = (
        'FRAG CopyNumber FragmentNumber Kilobytes Remainder'
        ' MediaType Density FileNumber IDPath Host'
        ' BlockSize Offset MediaDate DeviceWrittenOn f_flags '
        ' MediaDescriptor Expiration MPX RetentionLevel Checkpoint '
        ' ResumeNBR MediaSeq MediaSubtype TrytoKeepTime CopyCreationTime')

    fragline26 = coll.namedtuple('FRAG26', frag_line_base_name + ' Unused1')
    fragline27 = coll.namedtuple('FRAG27', frag_line_base_name + ' Unused1 KeyTag')
    fragline28 = coll.namedtuple('FRAG28', frag_line_base_name + ' Unused1 KeyTag STLtag')
    fragline31 = coll.namedtuple('FRAG31', frag_line_base_name +
                                 ' FragmentState DataFormat KeyTag STLtag MirrorParent CopyOnHold')

    frag_line_dict = {
        26: fragline26,
        27: fragline27,
        28: fragline28,
        31: fragline31, }

    if bp_lines[0].split()[0] == 'IMAGE':
        image_line_len = len(shlex.split(bp_lines[0]))
        imageline = image_line_dict[image_line_len]
    image_line = image_line_dict[image_line_len](*(shlex.split(bp_lines[0])))

    if bp_lines[2].split()[0] == 'FRAG':
        frag_line_len = len(shlex.split(bp_lines[2]))
        # print frag_line_len
        fragline = frag_line_dict[frag_line_len]
    frag_line = frag_line_dict[frag_line_len](*(shlex.split(bp_lines[2])))

    output_list = []

    for line in bp_lines:
        if line.split()[0] == 'IMAGE':
            image_line = imageline(*(shlex.split(line)))
            output_list.append(image_line._asdict())
        elif line.split()[0] == 'HISTO':
            pass
        elif line.split()[0] == 'FRAG':
            frag_line = fragline(*(shlex.split(line)))
            output_list.append(frag_line._asdict())

    return output_list


class BpImageList_Test(unittest.TestCase):
    def test_with_sampel_data(self):
        lines = ("IMAGE rhel-guest.nbappliance.lab 0 1 12 rhel-guest.nbappliance.lab_1464611509 Oracle_Copilot 4 "
                 "*NULL* oracle Full 0 9 1464611509 8 2147483647 0 0 3150848 9 1 1 0 Oracle_Copilot_1464611509_FULL.f "
                 "*NULL* *NULL* 0 1 0 0 0 orcl_1388827487_PROXY 0 0 0 0 0 0 0 *NULL* 0 0 0 *NULL* 65 1 0 4544 1 0 "
                 "*NULL* SnapSLP 3 1464611508 0 0 *NULL* *NULL* 1 1 0 0"
                 "\n"
                 "HISTO 0 0 0 0 0 0 0 0 0 0"
                 "\n"
                 "FRAG 1 1 3150848 0 0 0 0 /copilot1 copilot.nbappliance.lab 0 0 0 0 0 "
                 "remote_vxfs:1:vxfs:/shares/copilot1:NBU+2016.05.30.05h31m52s+Oracle_Copilot+10869:/shares/copilot1:"
                 "/tmp/_vrts_frzn_img__copilot1_10869_1:rhel-guest.nbappliance.lab_1464611508 2147483647 "
                 "0 0 0 0 0 0 0 1464611517 1 2 *NULL* *NULL* 0 0")
        lines = lines.split('\n')
        self.assertEqual(lines[1], 'HISTO 0 0 0 0 0 0 0 0 0 0')
        result = bpimagelist_analyze(lines)
        self.assertEqual(result[1]['Kilobytes'], '3150848')
