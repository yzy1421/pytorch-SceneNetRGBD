import torch
import torch.nn as nn
from torch.utils.serialization import load_lua
import numpy as np

#lua_unet = load_lua('../SCENENET_RESULTS_FOLDER_RERUN/NYUv2_TABLE/SCENENET_RGBD_EPOCH_10/converted_model.t7')



class UNetRGBD(nn.Module):
    def __init__(self):
        super(UNetRGBD, self).__init__()

        ''' RGB '''

        '''first block'''
        self.conv_rgb_3_32 = nn.Conv2d(3, 32, 3, 1, 1)
        self.bn_rgb_3_32 = nn.BatchNorm2d(32, track_running_stats=True)
        self.bn_rgb_3_32.training = False

        self.relu = nn.ReLU(inplace=True)

        self.conv_rgb_32_32 = nn.Conv2d(32, 32, 3, 1, 1)
        self.bn_rgb_32_32 = nn.BatchNorm2d(32, track_running_stats=True)
        self.bn_rgb_32_32.training = False

        self.pool = nn.MaxPool2d(2, 2)


        ''' second block '''
        self.conv_rgb_32_64 = nn.Conv2d(32, 64, 3, 1, 1)
        self.bn_rgb_32_64 = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_rgb_32_64.training = False


        self.conv_rgb_64_64 = nn.Conv2d(64, 64, 3, 1, 1)
        self.bn_rgb_64_64 = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_rgb_64_64.training = False



        ''' third block '''
        self.conv_rgb_64_128 = nn.Conv2d(64, 128, 3, 1, 1)
        self.bn_rgb_64_128 = nn.BatchNorm2d(128, track_running_stats=True)
        self.bn_rgb_64_128.training = False


        self.conv_rgb_128_128 = nn.Conv2d(128, 128, 3, 1, 1)
        self.bn_rgb_128_128 = nn.BatchNorm2d(128, track_running_stats=True)
        self.bn_rgb_128_128.training = False


        ''' fourth block '''
        self.conv_rgb_128_256 = nn.Conv2d(128, 256, 3, 1, 1)
        self.bn_rgb_128_256 = nn.BatchNorm2d(256, track_running_stats=True)
        self.bn_rgb_128_256.training = False

        self.conv_rgb_256_256 = nn.Conv2d(256, 256, 3, 1, 1)
        self.bn_rgb_256_256 = nn.BatchNorm2d(256, track_running_stats=True)
        self.bn_rgb_256_256.training = False


        ''' D '''

        '''first block'''

        self.conv_d_3_32 = nn.Conv2d(1, 32, 3, 1, 1)
        self.bn_d_3_32 = nn.BatchNorm2d(32, track_running_stats=True)
        self.bn_d_3_32.training = False

        self.conv_d_32_32 = nn.Conv2d(32, 32, 3, 1, 1)
        self.bn_d_32_32 = nn.BatchNorm2d(32, track_running_stats=True)
        self.bn_d_32_32.training = False


        ''' second block '''
        self.conv_d_32_64 = nn.Conv2d(32, 64, 3, 1, 1)
        self.bn_d_32_64 = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_d_32_64.training = False

        self.conv_d_64_64 = nn.Conv2d(64, 64, 3, 1, 1)
        self.bn_d_64_64 = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_d_64_64.training = False


        ''' third block '''

        self.conv_d_64_128 = nn.Conv2d(64, 128, 3, 1, 1)
        self.bn_d_64_128 = nn.BatchNorm2d(128, track_running_stats=True)
        self.bn_d_64_128.training = False

        self.conv_d_128_128 = nn.Conv2d(128, 128, 3, 1, 1)
        self.bn_d_128_128 = nn.BatchNorm2d(128, track_running_stats=True)
        self.bn_d_128_128.training = False

        ''' fourth block '''

        self.conv_d_128_256 = nn.Conv2d(128, 256, 3, 1, 1)
        self.bn_d_128_256 = nn.BatchNorm2d(256, track_running_stats=True)
        self.bn_d_128_256.training = False

        self.conv_d_256_256 = nn.Conv2d(256, 256, 3, 1, 1)
        self.bn_d_256_256 = nn.BatchNorm2d(256, track_running_stats=True)
        self.bn_d_256_256.training = False

        self.conv512_1024 = nn.Conv2d(512, 1024, 3, 1, 1)
        self.conv1024_512 = nn.Conv2d(1024, 512, 3, 1, 1)
        self.up = nn.Upsample(scale_factor=2, mode='nearest')

        self.conv_512_512 = nn.Conv2d(512, 512, 3, 1, 1)
        self.bn_512_512 = nn.BatchNorm2d(512, track_running_stats=True)
        self.bn_512_512.training = False

        self.conv_512_256 = nn.Conv2d(512, 256, 3, 1, 1)
        self.bn_512_256 = nn.BatchNorm2d(256, track_running_stats=True)
        self.bn_512_256.training = False

        self.conv_512_256_n = nn.Conv2d(512, 256, 3, 1, 1)
        self.bn_512_256_n = nn.BatchNorm2d(256, track_running_stats=True)
        self.bn_512_256_n.training = False

        self.conv_256_128 = nn.Conv2d(256, 128, 3, 1, 1)
        self.bn_256_128 = nn.BatchNorm2d(128, track_running_stats=True)
        self.bn_256_128.training = False

        self.conv_256_128_n = nn.Conv2d(256, 128, 3, 1, 1)
        self.bn_256_128_n = nn.BatchNorm2d(128, track_running_stats=True)
        self.bn_256_128_n.training = False

        self.conv_128_64 = nn.Conv2d(128, 64, 3, 1, 1)
        self.bn_128_64 = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_128_64.training = False


        self.conv_128_64_n = nn.Conv2d(128, 64, 3, 1, 1)
        self.bn_128_64_n = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_128_64_n.training = False

        self.conv_64_64 = nn.Conv2d(64, 64, 3, 1, 1)
        self.bn_64_64 = nn.BatchNorm2d(64, track_running_stats=True)
        self.bn_64_64.training = False

        self.conv_out_64 = nn.Conv2d(64, 14, 1, 1, 0)


    def copy_bn_layer(self, pytorch_bn_layer, torch_bn_layer):

        pytorch_bn_layer.weight.data.copy_(torch_bn_layer.weight)
        pytorch_bn_layer.bias.data.copy_(torch_bn_layer.bias)
        pytorch_bn_layer.running_mean.data.copy_(torch_bn_layer.running_mean)
        pytorch_bn_layer.running_var.data.copy_(torch_bn_layer.running_var)

    def copy_conv_layer(self, pytorch_conv_layer, torch_conv_layer):

        pytorch_conv_layer.weight.data.copy_(torch_conv_layer.weight)
        pytorch_conv_layer.bias.data.copy_(torch_conv_layer.bias)

    def copy_weights(self, lua_model_t7):

        # SCENENET_RESULTS_FOLDER_RERUN/NYUv2_TABLE/SCENENET_RGB_EPOCH_15/converted_model.t7

        self.lua_unet = load_lua(lua_model_t7)
        self.lua_unet.evaluate()

        self.first_block = self.lua_unet.get(0)

        self.first_rgb_block = self.first_block.get(0)
        self.first_d_block   = self.first_block.get(1)

        self.copy_conv_layer(self.conv_rgb_3_32, self.first_rgb_block.get(0))
        self.copy_bn_layer(self.bn_rgb_3_32, self.first_rgb_block.get(1))
        self.copy_conv_layer(self.conv_rgb_32_32, self.first_rgb_block.get(3))
        self.copy_bn_layer(self.bn_rgb_32_32, self.first_rgb_block.get(4))

        self.copy_conv_layer(self.conv_d_3_32, self.first_d_block.get(0))
        self.copy_bn_layer(self.bn_d_3_32, self.first_d_block.get(1))
        self.copy_conv_layer(self.conv_d_32_32, self.first_d_block.get(3))
        self.copy_bn_layer(self.bn_d_32_32, self.first_d_block.get(4))




        self.second_block = self.lua_unet.get(1).get(1).get(1)

        self.second_rgb_block = self.second_block.get(0)
        self.second_d_block = self.second_block.get(1)

        self.copy_conv_layer(self.conv_rgb_32_64, self.second_rgb_block.get(0))
        self.copy_bn_layer(self.bn_rgb_32_64, self.second_rgb_block.get(1))
        self.copy_conv_layer(self.conv_rgb_64_64, self.second_rgb_block.get(3))
        self.copy_bn_layer(self.bn_rgb_64_64, self.second_rgb_block.get(4))

        self.copy_conv_layer(self.conv_d_32_64, self.second_d_block.get(0))
        self.copy_bn_layer(self.bn_d_32_64, self.second_d_block.get(1))
        self.copy_conv_layer(self.conv_d_64_64, self.second_d_block.get(3))
        self.copy_bn_layer(self.bn_d_64_64, self.second_d_block.get(4))




        self.third_block = self.lua_unet.get(1).get(1).get(2).get(1).get(1)

        self.third_rgb_block = self.third_block.get(0)
        self.third_d_block = self.third_block.get(1)

        self.copy_conv_layer(self.conv_rgb_64_128, self.third_rgb_block.get(0))
        self.copy_bn_layer(self.bn_rgb_64_128, self.third_rgb_block.get(1))
        self.copy_conv_layer(self.conv_rgb_128_128, self.third_rgb_block.get(3))
        self.copy_bn_layer(self.bn_rgb_128_128, self.third_rgb_block.get(4))

        self.copy_conv_layer(self.conv_d_64_128, self.third_d_block.get(0))
        self.copy_bn_layer(self.bn_d_64_128, self.third_d_block.get(1))
        self.copy_conv_layer(self.conv_d_128_128, self.third_d_block.get(3))
        self.copy_bn_layer(self.bn_d_128_128, self.third_d_block.get(4))




        self.fourth_block = self.lua_unet.get(1).get(1).get(2).get(1).get(2).get(1).get(1)

        self.fourth_rgb_block = self.fourth_block.get(0)
        self.fourth_d_block = self.fourth_block.get(1)

        self.copy_conv_layer(self.conv_rgb_128_256, self.fourth_rgb_block.get(0))
        self.copy_bn_layer(self.bn_rgb_128_256, self.fourth_rgb_block.get(1))
        self.copy_conv_layer(self.conv_rgb_256_256, self.fourth_rgb_block.get(3))
        self.copy_bn_layer(self.bn_rgb_256_256, self.fourth_rgb_block.get(4))

        self.copy_conv_layer(self.conv_d_128_256, self.fourth_d_block.get(0))
        self.copy_bn_layer(self.bn_d_128_256, self.fourth_d_block.get(1))
        self.copy_conv_layer(self.conv_d_256_256, self.fourth_d_block.get(3))
        self.copy_bn_layer(self.bn_d_256_256, self.fourth_d_block.get(4))


        self.fifth_block = self.lua_unet.get(1).get(1).get(2).get(1).get(2).get(1).get(2)
        self.copy_conv_layer(self.conv512_1024, self.fifth_block.get(2))
        self.copy_conv_layer(self.conv1024_512, self.fifth_block.get(3))



        self.sixth_block = self.lua_unet.get(1).get(1).get(2).get(1).get(2).get(1).get(3)

        self.copy_conv_layer(self.conv_512_512, self.sixth_block.get(0))
        self.copy_bn_layer(self.bn_512_512, self.sixth_block.get(1))
        self.copy_conv_layer(self.conv_512_256, self.sixth_block.get(3))
        self.copy_bn_layer(self.bn_512_256, self.sixth_block.get(4))



        self.seventh_block = self.lua_unet.get(1).get(1).get(2).get(1).get(5)

        self.copy_conv_layer(self.conv_512_256_n, self.seventh_block.get(0))
        self.copy_bn_layer(self.bn_512_256_n, self.seventh_block.get(1))
        self.copy_conv_layer(self.conv_256_128, self.seventh_block.get(3))
        self.copy_bn_layer(self.bn_256_128, self.seventh_block.get(4))


        self.eigth_block = self.lua_unet.get(1).get(1).get(5)

        self.copy_conv_layer(self.conv_256_128_n, self.eigth_block.get(0))
        self.copy_bn_layer(self.bn_256_128_n, self.eigth_block.get(1))
        self.copy_conv_layer(self.conv_128_64, self.eigth_block.get(3))
        self.copy_bn_layer(self.bn_128_64, self.eigth_block.get(4))


        self.ninth_block = self.lua_unet.get(4)

        self.copy_conv_layer(self.conv_128_64_n, self.ninth_block.get(0))
        self.copy_bn_layer(self.bn_128_64_n, self.ninth_block.get(1))
        self.copy_conv_layer(self.conv_64_64, self.ninth_block.get(3))
        self.copy_bn_layer(self.bn_64_64, self.ninth_block.get(4))

        self.tenth_block = self.lua_unet.get(5)
        self.copy_conv_layer(self.conv_out_64, self.tenth_block)


        print('Have copied the weights of the first block')


    def run_torch_pytorch_import_test(self):

        # Batch should be in NCHW format
        # input = np.ones((1, 3, 128, 128))
        input_rgb = np.random.rand(1, 3, 128, 128)
        myrgbImg = torch.tensor(input_rgb, dtype=torch.float32)

        input_d = np.random.rand(1, 1, 128, 128)
        mydImg = torch.tensor(input_d, dtype=torch.float32)

        yTorch_rgb = self.lua_unet.forward((myrgbImg, mydImg))

        ypyTorch_rgb = self.forward((myrgbImg, mydImg))

        print('ypTorch_rgb shape = ', ypyTorch_rgb.detach().numpy().shape)

        print('DIFF {}'.format(np.sum(yTorch_rgb.detach().numpy() - ypyTorch_rgb.detach().numpy())))

    def forward(self, x):

        ''' RGB '''

        ''' first block '''

        out_rgb = self.conv_rgb_3_32(x[0])
        out_rgb = self.bn_rgb_3_32(out_rgb)
        out_rgb = self.relu(out_rgb)
        out_rgb = self.conv_rgb_32_32(out_rgb)
        out_rgb = self.bn_rgb_32_32(out_rgb)
        out_rgb_relu32 = self.relu(out_rgb)

        out_rgb = self.pool(out_rgb_relu32)

        ''' second block '''

        out_rgb = self.conv_rgb_32_64(out_rgb)
        out_rgb = self.bn_rgb_32_64(out_rgb)
        out_rgb = self.relu(out_rgb)
        out_rgb = self.conv_rgb_64_64(out_rgb)
        out_rgb = self.bn_rgb_64_64(out_rgb)
        out_rgb_relu64 = self.relu(out_rgb)

        out_rgb = self.pool(out_rgb_relu64)

        ''' third block '''

        out_rgb = self.conv_rgb_64_128(out_rgb)
        out_rgb = self.bn_rgb_64_128(out_rgb)
        out_rgb = self.relu(out_rgb)
        out_rgb = self.conv_rgb_128_128(out_rgb)
        out_rgb = self.bn_rgb_128_128(out_rgb)
        out_rgb_relu128 = self.relu(out_rgb)

        out_rgb = self.pool(out_rgb_relu128)


        ''' fourth block '''

        out_rgb = self.conv_rgb_128_256(out_rgb)
        out_rgb = self.bn_rgb_128_256(out_rgb)
        out_rgb = self.relu(out_rgb)
        out_rgb = self.conv_rgb_256_256(out_rgb)
        out_rgb = self.bn_rgb_256_256(out_rgb)
        out_rgb_relu256 = self.relu(out_rgb)

        out_rgb = out_rgb_relu256



        ''' D '''

        '''first block '''

        out_d = self.conv_d_3_32(x[1])
        out_d = self.bn_d_3_32(out_d)
        out_d = self.relu(out_d)
        out_d = self.conv_d_32_32(out_d)
        out_d = self.bn_d_32_32(out_d)
        out_d_relu32 = self.relu(out_d)

        out_d = self.pool(out_d_relu32)

        ''' second block '''

        out_d = self.conv_d_32_64(out_d)
        out_d = self.bn_d_32_64(out_d)
        out_d = self.relu(out_d)
        out_d = self.conv_d_64_64(out_d)
        out_d = self.bn_d_64_64(out_d)
        out_d_relu64 = self.relu(out_d)

        out_d = self.pool(out_d_relu64)

        ''' third block '''

        out_d = self.conv_d_64_128(out_d)
        out_d = self.bn_d_64_128(out_d)
        out_d = self.relu(out_d)
        out_d = self.conv_d_128_128(out_d)
        out_d = self.bn_d_128_128(out_d)
        out_d_relu128 = self.relu(out_d)

        out_d = self.pool(out_d_relu128)


        ''' fourth '''

        out_d = self.conv_d_128_256(out_d)
        out_d = self.bn_d_128_256(out_d)
        out_d = self.relu(out_d)
        out_d = self.conv_d_256_256(out_d)
        out_d = self.bn_d_256_256(out_d)
        out_d_relu256 = self.relu(out_d)

        out_d = out_d_relu256


        ''' RGBD '''

        out = torch.cat([out_rgb, out_d], dim=1)

        out = self.pool(out)
        out = self.conv512_1024(out)
        out = self.conv1024_512(out)
        out = self.up(out)


        out = self.conv_512_512(out)
        out = self.bn_512_512(out)
        out = self.relu(out)

        out = self.conv_512_256(out)
        out = self.bn_512_256(out)
        out = self.relu(out)

        out = self.up(out)
        

        out = torch.cat([out_rgb_relu128, out_d_relu128, out], dim=1)
        out = self.conv_512_256_n(out)
        out = self.bn_512_256_n(out)
        out = self.relu(out)

        out = self.conv_256_128(out)
        out = self.bn_256_128(out)
        out = self.relu(out)

        out = self.up(out)


        out = torch.cat([out_rgb_relu64, out_d_relu64, out], dim=1)
        out = self.conv_256_128_n(out)
        out = self.bn_256_128_n(out)
        out = self.relu(out)

        out = self.conv_128_64(out)
        out = self.bn_128_64(out)
        out = self.relu(out)

        out = self.up(out)

        out = torch.cat([out_rgb_relu32, out_d_relu32, out], dim=1)
        out = self.conv_128_64_n(out)
        out = self.bn_128_64_n(out)
        out = self.relu(out)

        out = self.conv_64_64(out)
        out = self.bn_64_64(out)
        out = self.relu(out)

        out = self.conv_out_64(out)


        return out