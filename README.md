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

Currently we use Jupyter notebooks for showing the functions and providing programming examples. The notebooks are located under `notebooks` directory.

Nun ni uzas Jupiter kvaterojn pro montri la functiojn kaj doni egzemplojn de programi. La kvateroj troviĝas en dosiero `notebooks`.

本软件包目前使用 Jupyter 笔记本提供用户界面，并给出编程示例。这些笔记本文件存放在 `notebooks` 目录中。

### Using vscode / Uzante vscode / 使用 vscode

Vscode recognizes the virtual environment you use. For a better experience, you might consider run it with the Jupyter plugin. Then just open the codebase directory in your vscode, and open the notebook file therein.

Vscode scias la venv-on kiun vi uzas. Por uzi ĝin pli bone, estus facile funktionigi uzante `Jupyter` aldonaĵon. Poste, malfermu la dosieron en vscode, kaj malfermu la kvateron.

Vscode 可识别虚拟环境。为增强使用体验，可使用 Jupyter 扩展。装好后，在打开本软件包目录的 vscode 窗口中打开相应文件即可。

### Using Jupyter server / Uzante 'Jupyter' servilo / 使用 Jupyter 服务

You just serve it with

Oni nur bezonas

运行以下命令即可

```bash
  jupyter notebook filename.ipynb
```

### Reference Note / 参考文献

If you intend to utilize this package for scientific research and publish papers, please kindly include the citation of the following reference:

Zhang, L., He, J., Zhao, J., Yao, S., & Feng, X. (2018). Nature of magnetic holes above ion scales: a mixture of stable slow magnetosonic and unstable mirror modes in a double-polytropic scenario? The Astrophysical Journal, 864(1), 35.


### Contact Info /联系信息
Dr. Lei ZHANG: beatlesfan1987@gmail.com

Dr. Jiansen HE: jshept@gmail.com
