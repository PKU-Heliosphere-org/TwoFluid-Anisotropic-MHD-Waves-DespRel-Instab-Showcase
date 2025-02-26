This only serves as a teaching meterial.

For research purposes, please use plasma-calc-tool instead.

No further features (GPU acceleration, ADT model generation ...) will be considered mainstreamly (though sometimes backports may or may not apply).

Ĉi tiu paketo de programo nur agas por la instruo de la kurso je PKU.

Bonvolu uzi plasma-calc-tool antaŭe se vi volas kalkuli pli formale.

Mi ne devos aldoni iujn funktiojn en ĉi tiun paketon, ktp. GPU aŭ ADT.

小型软件包，适用于教学演示目的。主要维护的研究用代码包是 plasma-calc-tool. 本软件包不保证性能与功能的主要开发。

# Quick start / Rapida Komenco / 快速设置方法

This package is a standard PyPI project (though not released there) and can be installed with Pip. A virtual environment is recommended. Thence you may start with

Ĉi tiu paketo funkcias kun PyPI (krome ne vidiĝinda tie). Oni povas funkcigi ĝin por Pip. Mi rekomendas uzi venv-on. Oni povas komenci per

本软件按 PyPI 规范打包（虽然不准备提交到 PyPI），可用 pip 安装。建议使用虚拟环境安装及运行。因而，可使用

```bash
virtualenv venv
. venv/bin/activate
pip install -e .
```

and test with

kaj fari ĝiajn testojn per

并运行单元测试

```bash
pip install pytest pytest-cov
pytest -s .
```

## User Interface / Uzanta Interfaco / 用户界面
