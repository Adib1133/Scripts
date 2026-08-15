# Image Enhancement & Upscaling

A Python/Jupyter Notebook image-processing pipeline for improving low-quality images through denoising, sharpening, optional contrast/color enhancement, and high-quality upscaling.

The notebook uses a **5-stage enhancement pipeline** built primarily with OpenCV, Pillow, NumPy, and Matplotlib.

## Features

- Load and inspect an input image.
- Display image resolution, file size, and channel information.
- Reduce image noise using **Non-Local Means denoising** in L\*a\*b color space.
- Sharpen image details using **unsharp masking**.
- Optionally improve local contrast with **CLAHE**.
- Optionally increase color saturation.
- Upscale images using **Lanczos interpolation**.
- Apply a bilateral filter after upscaling to reduce ringing and preserve edges.
- Compare images before and after each processing stage.
- Generate RGB histogram comparisons.
- Automatically generate an output filename.
- Report processing settings, output resolution, and file size.

## Processing Pipeline

The notebook processes an image through the following stages:

| Stage | Technique | Purpose |
| --- | --- | --- |
| 1 | Load & Inspect | Load the image and inspect its properties |
| 2 | Non-Local Means | Reduce noise while preserving image structure |
| 3 | Unsharp Masking | Improve edge and detail crispness |
| 4 | CLAHE + Saturation | Improve local contrast and color when enabled |
| 5 | Lanczos + Bilateral Filter | Upscale and refine the enlarged image |

The stages are controlled through configuration flags, so denoising, sharpening, and color enhancement can independently be enabled or disabled.

## Requirements

- Python 3.x
- Jupyter Notebook or JupyterLab
- OpenCV
- Pillow
- NumPy
- Matplotlib

Install the dependencies with:

```bash
pip install opencv-python-headless Pillow numpy matplotlib
```

The notebook also contains an installation cell that can install these packages automatically.

## Project Structure

A typical setup is:

```text
project-folder/
├── Enhancher.ipynb
└── your_image.jpg
```

After execution, the enhanced image is normally saved in the same directory:

```text
project-folder/
├── Enhancher.ipynb
├── your_image.jpg
└── your_image_enhanced_8x.jpg
```

## Usage

### 1. Open the Notebook

Open:

```text
Enhancher.ipynb
```

in Jupyter Notebook, JupyterLab, or a compatible notebook environment.

### 2. Place Your Image

Put the image you want to enhance in the same directory as the notebook.

By default, the notebook expects:

```text
your_image.jpg
```

### 3. Configure the Input

Edit the configuration section:

```python
INPUT_FILENAME = 'your_image.jpg'
OUTPUT_PATH = None
```

`OUTPUT_PATH = None` enables automatic output filename generation.

### 4. Configure Enhancement Parameters

The notebook provides the following parameters:

```python
SCALE          = 8.0
DENOISE_STR    = 8
SHARPEN_AMOUNT = 1.5
CLAHE_CLIP     = 2.5
SATURATION     = 1.25
```

You can also enable or disable individual stages:

```python
DO_DENOISE = True
DO_SHARPEN = True
DO_COLOR   = False
```

### 5. Run the Notebook

Execute the cells from top to bottom.

The notebook displays intermediate comparisons so you can visually inspect the effect of each enabled processing stage.

## Configuration Reference

### `SCALE`

Controls the enlargement factor.

Examples:

```python
SCALE = 2.0   # 2×
SCALE = 4.0   # 4×
SCALE = 8.0   # 8×
```

The current notebook is configured for:

```python
SCALE = 8.0
```

Higher scaling factors produce substantially larger images and may require more memory and processing time.

### `DENOISE_STR`

Controls Non-Local Means denoising strength.

General guidance:

| Value | Effect |
| --- | --- |
| `0` | Minimal/off |
| `1–5` | Mild denoising |
| `6–12` | Strong denoising |

Default:

```python
DENOISE_STR = 8
```

The luminance channel is denoised more aggressively than the chroma channels to reduce color smearing.

### `SHARPEN_AMOUNT`

Controls unsharp-mask intensity.

Example:

```python
SHARPEN_AMOUNT = 1.0   # Essentially no sharpening
SHARPEN_AMOUNT = 1.5   # Mild sharpening
SHARPEN_AMOUNT = 2.5   # Strong sharpening
```

Default:

```python
SHARPEN_AMOUNT = 1.5
```

Excessive sharpening can create halos or emphasize compression artifacts, so this parameter should be adjusted according to the source image.

### `CLAHE_CLIP`

Controls the CLAHE local contrast enhancement strength.

Default:

```python
CLAHE_CLIP = 2.5
```

The notebook applies CLAHE to the luminance channel rather than directly altering all RGB channels.

### `SATURATION`

Controls color saturation.

```python
SATURATION = 1.0    # No change
SATURATION = 1.25   # Moderate increase
```

The current default is:

```python
SATURATION = 1.25
```

Color enhancement must first be enabled:

```python
DO_COLOR = True
```

## Image Processing Details

### Denoising

The denoising stage converts the image from BGR to L\*a\*b color space and applies OpenCV's Fast Non-Local Means Denoising separately to the luminance and chroma channels.

This approach is intended to reduce noise while helping preserve color boundaries and image details.

### Sharpening

Sharpening uses an unsharp-mask approach:

1. Create a Gaussian-blurred version of the image.
2. Combine the original and blurred images with weighted subtraction.
3. Clip the result to the valid 8-bit image range.

The blur radius automatically scales with the image dimensions.

### Contrast and Color Enhancement

When enabled, this stage:

1. Converts the image to L\*a\*b.
2. Applies CLAHE to the luminance channel.
3. Converts the result to HSV.
4. Multiplies the saturation channel by the configured saturation factor.
5. Converts the result back to BGR.

This stage is disabled by default:

```python
DO_COLOR = False
```

### Upscaling

The upscaling stage uses Pillow's **LANCZOS** resampling algorithm.

After enlargement, OpenCV's bilateral filter is applied to help reduce ringing artifacts while retaining edges.

This is a conventional interpolation-based enhancement workflow; it is **not a machine-learning or AI super-resolution model**.

## Output

If no custom output path is supplied, the notebook automatically generates a filename based on the input image:

```text
<input-name>_enhanced_<scale>x.<extension>
```

For example:

```text
your_image.jpg
```

with:

```python
SCALE = 8.0
```

produces:

```text
your_image_enhanced_8x.jpg
```

For JPEG output, the notebook uses quality `95`.

For PNG output, compression level `6` is used.

For WebP output, quality `95` is used.

## Image Analysis

The notebook provides side-by-side comparisons showing:

- Original image
- Image after denoising
- Image after sharpening
- Image after optional color/contrast enhancement
- Final enhanced and upscaled image

It also generates an RGB histogram comparison between the original and final images.

The histogram displays pixel-intensity distributions for:

- Blue
- Green
- Red

## Example Summary

At the end of execution, the notebook prints a summary similar to:

```text
================================================
         ENHANCEMENT SUMMARY
================================================
  Input   : ...
  Output  : ...
  Resolution : 640×480  →  5120×3840  (×8)
  File size  : ... KB  →  ... KB
------------------------------------------------
  Denoise : ON  (strength=8)
  Sharpen : ON  (amount=1.5)
  Color   : OFF
  Upscale : ×8  (Lanczos + bilateral)
================================================
```

The actual values depend on the selected image and configuration.

## Supported Image Formats

The notebook relies on OpenCV/Pillow image loading and saving capabilities. Common formats such as the following can be used:

- JPEG / JPG
- PNG
- WebP

The output format is determined by the extension specified in `OUTPUT_PATH`, or by the original input extension when the output path is generated automatically.

## Performance Considerations

Processing time depends on:

- Original image resolution
- Upscaling factor
- Denoising strength
- Enabled processing stages
- Available CPU and memory

Non-Local Means denoising can be computationally expensive, especially for large images.

Large scaling factors can also produce very large output images. For example:

```text
2000 × 1500 at 8×
```

becomes:

```text
16000 × 12000
```

Such images can require significant memory and storage.

## Limitations

This notebook performs traditional image processing rather than AI-based image reconstruction.

Consequently:

- It cannot reliably recover details that are completely absent from the source image.
- Upscaling increases pixel dimensions but does not create genuinely captured high-resolution information.
- Heavy JPEG compression artifacts may remain.
- Excessive sharpening can introduce halos or emphasize noise.
- Excessive denoising can remove fine texture.
- Very large scale factors can consume substantial memory.
- Results depend strongly on the quality and characteristics of the source image.

## Recommended Settings

For a general-purpose enhancement workflow:

```python
SCALE          = 4.0
DENOISE_STR    = 6
SHARPEN_AMOUNT = 1.5
CLAHE_CLIP     = 2.0
SATURATION     = 1.15

DO_DENOISE = True
DO_SHARPEN = True
DO_COLOR   = False
```

For stronger enlargement, the notebook's current configuration can be used:

```python
SCALE          = 8.0
DENOISE_STR    = 8
SHARPEN_AMOUNT = 1.5
CLAHE_CLIP     = 2.5
SATURATION     = 1.25
```

If the source image already has strong colors or visible noise, consider using lower sharpening and saturation values.

## License

This project is for internal workplace use.

## Author

Created as a workplace automation tool for processing and upscaling basic passport size images.