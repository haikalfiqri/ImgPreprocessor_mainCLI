"""
Main Image Preprocessing Program
=================================
CLI entry point that imports preprocessing functions from
imagepreproc_haikalfiqri.preprocessing
"""
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

#need a handler function for noise reduction


#need a handler function for image resizing



def main() -> int:
    """Main program - lets user choose which preprocessing module to run."""
    
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
                # Call the color conversion handler
            elif choice == "2":
                # Call the noise reduction handler
            elif choice == "3":
                # Call the image resizing handler
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