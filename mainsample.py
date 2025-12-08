"""
Main Image Preprocessing Program
=================================
CLI entry point that imports preprocessing functions from
imagepreproc_haikalfiqri.preprocessing
"""
import cv2
import sys
from PIL import Image
from imagepreproc_haikalfiqri import preprocessing

def display_main_menu() -> None:
    """Display the main menu options."""
    print("\n" + "=" * 70)
    print("IMAGE PREPROCESSING TOOLKIT")
    print("=" * 70)
    print("\nSelect which preprocessing module to run:")
    print("1. Color Space Conversion (BGR to RGB/GRAY/HSV/LAB)")
    print("2. Noise Reduction (Gaussian/Median/Bilateral filters)")
    print("3. Image Resizing (OpenCV & Pillow)")
    print("4. Exit Program")
    print("=" * 70)


def load_bgr_image_from_user() -> tuple[str, cv2.Mat | None]:
    """Prompt user for image path and load it as BGR OpenCV image."""
    path = input("\nEnter image file path: ").strip()
    if not path:
        print("No path given.")
        return path, None

    image = cv2.imread(path)
    if image is None:
        print(f"Could not read image from '{path}'.")
        return path, None

    return path, image


def show_opencv_image(title: str, image) -> None:
    """Display an image using OpenCV and wait for a key press."""
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imshow / waitKey pattern is standard for showing images.[web:57][web:60]


#need a handler function for color conversion
def handle_color_conversion() -> None:
    """Menu handler for color space conversion."""
    path, bgr = load_bgr_image_from_user()
    if bgr is None:
        return

    print("\nChoose color space:")
    print("1. RGB")
    print("2. GRAY")
    print("3. HSV")
    print("4. LAB")
    mode_choice = input("Enter your choice (1-4): ").strip()

    mode_map = {
        "1": "rgb",
        "2": "gray",
        "3": "hsv",
        "4": "lab",
    }
    mode = mode_map.get(mode_choice)
    if mode is None:
        print("Invalid color space choice.")
        return

    try:
        converted = preprocessing.convert_color(bgr, mode=mode)
    except Exception as e:
        print(f"Error during color conversion: {e}")
        return

    show_opencv_image(f"{mode.upper()} - {path}", preprocessing.resize_for_display(converted))

def denoise_reduction() -> None:
    path, bgr = load_bgr_image_from_user()
    if bgr is None:
        return

    print("\nChoose noise reduction filter:")
    print("1. Gaussian Blur")
    print("2. Median Blur")
    print("3. Bilateral Filter")
    filter_choice = input("Enter your choice (1-3): ").strip()

    if filter_choice == "1":
        ksize = int(input("Enter kernel size (odd number, e.g. 3,5,7,11): ").strip() or "11")
        result = preprocessing.denoise_gaussian(bgr, ksize=ksize)
    elif filter_choice == "2":
        ksize = int(input("Enter kernel size (odd number, e.g. 3,5,7,11): ").strip() or "11")
        result = preprocessing.denoise_median(bgr, ksize=ksize)
    elif filter_choice == "3":
        d = int(input("Enter diameter d (e.g. 15): ").strip() or "15")
        sigma_color = int(input("Enter sigmaColor (e.g. 100): ").strip() or "100")
        sigma_space = int(input("Enter sigmaSpace (e.g. 100): ").strip() or "100")
        result = preprocessing.denoise_bilateral(
            bgr,
            d=d,
            sigma_color=sigma_color,
            sigma_space=sigma_space,
        )
    else:
        print("Invalid filter choice.")
        return

    show_opencv_image(f"Denoised - {path}", preprocessing.resize_for_display(result))


#need a handler function for image resizing
def handle_image_resizing() -> None:
    """Menu handler for image resizing using OpenCV or Pillow."""
    print("\nChoose backend:")
    print("1. OpenCV")
    print("2. Pillow (PIL)")
    backend_choice = input("Enter your choice (1-2): ").strip()

    path = input("\nEnter image file path: ").strip()
    if not path:
        print("No path given.")
        return

    try:
        width = int(input("Enter target width (pixels): ").strip())
        height = int(input("Enter target height (pixels): ").strip())
    except ValueError:
        print("Width and height must be integers.")
        return

    if backend_choice == "1":
        # OpenCV backend.
        bgr = cv2.imread(path)
        if bgr is None:
            print(f"Could not read image from '{path}'.")
            return
        resized = preprocessing.resize_opencv(bgr, width=width, height=height)
        show_opencv_image(f"Resized (OpenCV) - {path}", resized)
    elif backend_choice == "2":
        # Pillow backend.
        try:
            pil_img = Image.open(path)
        except Exception as e:
            print(f"Could not open image with Pillow: {e}")
            return
        resized_pil = preprocessing.resize_pillow(pil_img, width=width, height=height)
        resized_pil.show()  # Pillow’s simple display helper.[web:49]
    else:
        print("Invalid backend choice.")
        return



def main() -> int:
    """Main program - lets user choose which preprocessing module to run."""
    print("\n" + "=" * 70)
    print("   WELCOME TO IMAGE PREPROCESSING TOOLKIT")
    print("=" * 70)
    print("\nThis tool provides three preprocessing modules:")
    print("• Color Space Conversion - Transform color representations")
    print("• Noise Reduction - Remove unwanted noise from images")
    print("• Image Resizing - Change image dimensions")
    print("\nEach module uses functions from the imagepreproc_haikalfiqri library.")

    while True:
        display_main_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "4":
            print("\n" + "=" * 70)
            print("Thank you for using Image Preprocessing Toolkit!")
            print("=" * 70)
            return 0

        if choice not in {"1", "2", "3"}:
            print("Invalid choice. Please select 1, 2, 3, or 4.")
            continue

        try:
            if choice == "1":
                handle_color_conversion()
            elif choice == "2":
                denoise_reduction()
            elif choice == "3":
                 handle_image_resizing()
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Returning to main menu...")

        print("\n" + "-" * 70)
        continue_choice = input("Run another module? (y/n): ").strip().lower()
        if continue_choice in {"n", "no"}:
            print("\n" + "=" * 70)
            print("Thank you for using Image Preprocessing Toolkit!")
            print("=" * 70)
            return 0


if __name__ == "__main__":
    sys.exit(main())