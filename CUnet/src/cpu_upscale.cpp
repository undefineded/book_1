// RGB-only CPU inference adapter for waifu2x CUnet, scale=2, noise=-1.
// Tile padding/cropping follows nihui/waifu2x-ncnn-vulkan (MIT license).
// https://github.com/nihui/waifu2x-ncnn-vulkan
// Dependency: https://github.com/Tencent/ncnn (BSD 3-Clause).
// Shared source: build with CUnet/build.sh; see CUnet/README.md.
#include <net.h>
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

static std::string token(std::istream& in) {
    std::string s;
    while (in >> s) {
        if (s[0] == '#') { std::getline(in, s); continue; }
        return s;
    }
    throw std::runtime_error("Invalid PPM header");
}

int main(int argc, char** argv) {
    if (argc != 4) { std::cerr << "input.ppm output.ppm model-directory\n"; return 1; }
    std::ifstream input(argv[1], std::ios::binary);
    if (token(input) != "P6") return 2;
    const int w = std::stoi(token(input)), h = std::stoi(token(input));
    if (token(input) != "255") return 3;
    input.get();
    std::vector<unsigned char> pixels((size_t)w*h*3), result((size_t)w*h*12);
    input.read((char*)pixels.data(), pixels.size());
    if ((size_t)input.gcount() != pixels.size()) return 4;
    ncnn::Net net;
    net.opt.num_threads = 2;
    net.opt.use_vulkan_compute = false;
    net.opt.use_fp16_packed = false;
    net.opt.use_fp16_storage = false;
    net.opt.use_fp16_arithmetic = false;
    net.opt.use_bf16_storage = false;
    std::string model = argv[3];
    if (net.load_param((model+"/scale2.0x_model.param").c_str()) != 0) return 5;
    if (net.load_model((model+"/scale2.0x_model.bin").c_str()) != 0) return 6;
    const int tile = 256, pad = 18;
    const float norm[3] = {1.f/255, 1.f/255, 1.f/255};
    for (int y=0; y<h; y+=tile) for (int x=0; x<w; x+=tile) {
        int tw=std::min(tile,w-x), th=std::min(tile,h-y);
        int pr=pad+tw%2, pb=pad+th%2;
        int x0=std::max(x-pad,0), y0=std::max(y-pad,0);
        int x1=std::min(x+tile+pr,w), y1=std::min(y+tile+pb,h);
        ncnn::Mat in=ncnn::Mat::from_pixels_roi(pixels.data(), ncnn::Mat::PIXEL_RGB,w,h,x0,y0,x1-x0,y1-y0);
        in.substract_mean_normalize(nullptr,norm);
        ncnn::Mat padded;
        int pt=std::max(pad-y,0), pl=std::max(pad-x,0);
        int pbottom=std::max(std::min(y+tile+pb-h,pb),0);
        int pright=std::max(std::min(x+tile+pr-w,pr),0);
        ncnn::copy_make_border(in,padded,pt,pbottom,pl,pright,ncnn::BORDER_REPLICATE,0.f,net.opt);
        auto ex=net.create_extractor();
        if (ex.input("Input1",padded) != 0) return 7;
        ncnn::Mat out;
        if (ex.extract("Eltwise4",out) != 0) return 8;
        if (out.w<tw*2 || out.h<th*2 || out.c!=3 || out.elemsize!=4u) {
            std::cerr<<"Unexpected output "<<out.w<<","<<out.h<<","<<out.c<<","<<out.elemsize<<"\n";return 9;
        }
        for (int q=0;q<3;q++) for(int iy=0;iy<th*2;iy++) {
            const float* row=out.channel(q).row(iy);
            for(int ix=0;ix<tw*2;ix++) {
                int v=(int)(row[ix]*255.f+0.5f);
                result[((size_t)(y*2+iy)*w*2+x*2+ix)*3+q]=(unsigned char)std::clamp(v,0,255);
            }
        }
    }
    std::ofstream output(argv[2],std::ios::binary);
    output<<"P6\n"<<w*2<<" "<<h*2<<"\n255\n";
    output.write((const char*)result.data(),result.size());
    return output.good()?0:10;
}
