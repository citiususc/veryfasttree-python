import os
import shutil
import cmake
import platform
import subprocess
import requests, zipfile, io

VERSION = '4.0.4'


def cmake_run(*args):
    subprocess.check_call([os.path.join(cmake.CMAKE_BIN_DIR, 'cmake'), *args], env=os.environ)


if os.path.exists('c'):
    shutil.rmtree('c')

r = requests.get(f'https://github.com/citiususc/veryfasttree/archive/refs/tags/v{VERSION}.zip')
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall('c')

is_x86_64 = platform.machine() == 'x86_64' or platform.machine() == 'AMD64'

# Apple Clang has not native support for OpenMP
if platform.system() == 'Darwin':
    print('On error check if OpenMP is installed or install with "brew install libomp" and use "export VFT_OMP=brew"')
    if 'VFT_OMP' in os.environ:
        omp_path = os.environ['VFT_OMP']

        if omp_path == 'brew':
            omp_path = subprocess.check_output(['brew', '--prefix', 'libomp'], text=True).strip()

        if 'CXXFLAGS' in os.environ:
            os.environ['CXXFLAGS'] += f' -I{omp_path}/include'
        else:
            os.environ['CXXFLAGS'] = f'-I{omp_path}/include'

        if 'LDFLAGS' in os.environ:
            os.environ['LDFLAGS'] += f' {omp_path}/lib/libomp.a'
        else:
            os.environ['LDFLAGS'] = f'{omp_path}/lib/libomp.a'

for option, simb in [('USE_SEE2', 'sse2')] + ([('USE_AVX2', 'avx2'), ('USE_AVX512', 'avx512f')] if is_x86_64 else []):
    cmake_run('-DUSE_NATIVE=OFF', f'-D{option}=ON', '-B', 'c/build' + simb, '-S', f'c/veryfasttree-{VERSION}')
    cmake_run('--build', 'c/build' + simb, '--config', 'Release')
    cmake_run('--install', 'c/build' + simb, '--prefix', 'veryfasttree')

    for file in os.listdir('veryfasttree/bin'):
        if file.startswith('VeryFastTree') and not file.startswith('VeryFastTree-'):
            new_name = file.replace('VeryFastTree', 'VeryFastTree-' + simb)
            os.rename(os.path.join('veryfasttree/bin', file), os.path.join('veryfasttree/bin', new_name))
            break

shutil.rmtree('c')
