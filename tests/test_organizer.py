import pytest
from organize.file_organizer import FileOrganizer


@pytest.fixture
def setup_test_environment(tmp_path):
    # Setup a temporary directory with some test files
    file_data = [
        ("test1.txt", b"Sample content 1"),
        ("test2.txt", b"Sample content 2"),
        ("duplicate_test1.txt", b"Sample content 1"),  # Duplicate of test1.txt
        ("image1.jpg", b"Image content"),
        ("doc1.docx", b"Document content"),
        ("no_extension_file", b"No extension content"),
    ]

    for file_name, content in file_data:
        file_path = tmp_path / file_name
        with open(file_path, "wb") as f:
            f.write(content)

    return tmp_path


def test_organize_files_by_extension(setup_test_environment):
    folder_path = str(setup_test_environment)
    organizer = FileOrganizer(folder_path)

    total_files, processed_files = organizer.organize()

    # Verify that files were moved to correct folders
    txt_folder = setup_test_environment / "txt"
    jpg_folder = setup_test_environment / "jpg"
    docx_folder = setup_test_environment / "docx"
    duplicate_folder = setup_test_environment / "Duplicates"

    assert txt_folder.exists(), "Text files folder should be created."
    assert jpg_folder.exists(), "Image files folder should be created."
    assert docx_folder.exists(), "Document files folder should be created."
    assert duplicate_folder.exists(), "Duplicates folder should be created."

    # Check that files were correctly moved
    assert (txt_folder / "test1.txt").exists(), "test1.txt should be in the txt folder."
    assert (txt_folder / "test2.txt").exists(), "test2.txt should be in the txt folder."
    assert (
        jpg_folder / "image1.jpg"
    ).exists(), "image1.jpg should be in the jpg folder."
    assert (
        docx_folder / "doc1.docx"
    ).exists(), "doc1.docx should be in the docx folder."

    # Check duplicates
    assert (
        duplicate_folder / "duplicate_test1.txt"
    ).exists(), "Duplicate file should be moved to Duplicates folder."

    # Check the total and processed file count
    assert total_files == 6, f"Expected 6 total files, but found {total_files}."
    assert (
        processed_files == 6
    ), f"Expected 6 processed files, but found {processed_files}."


def test_file_without_extension(setup_test_environment):
    folder_path = str(setup_test_environment)
    organizer = FileOrganizer(folder_path)

    organizer.organize()

    # Check if the file without an extension is not moved
    no_extension_file = setup_test_environment / "no_extension_file"
    assert no_extension_file.exists(), "File without extension should remain unmoved."

    report = organizer.get_report()
    assert (
        "doesn't have an extension, skipping." in report["details"][3]
    ), "Report should mention the skipped file."


def test_duplicate_file_detection(setup_test_environment):
    folder_path = str(setup_test_environment)
    organizer = FileOrganizer(folder_path)

    organizer.organize()

    # Verify that the duplicate file is in the Duplicates folder
    duplicate_folder = setup_test_environment / "Duplicates"
    assert (
        duplicate_folder / "duplicate_test1.txt"
    ).exists(), "Duplicate should be moved to Duplicates folder."

    # Check if the original file remains in its correct folder
    txt_folder = setup_test_environment / "txt"
    assert (
        txt_folder / "test1.txt"
    ).exists(), "Original file should remain in the txt folder."


def test_report_generation(setup_test_environment):
    folder_path = str(setup_test_environment)
    organizer = FileOrganizer(folder_path)

    organizer.organize()
    report = organizer.get_report()

    # Verify that the report contains the expected summary
    summary = report["summary"]
    assert any(
        "Moved" in s for s in summary
    ), "Report should contain information about moved files."

    # Verify the details of the report
    details = report["details"]
    assert len(details) > 0, "There should be details about the files processed."
    assert "Moved test1.txt to" in details[0], "First move should be reported."


def test_move_count(setup_test_environment):
    folder_path = str(setup_test_environment)
    organizer = FileOrganizer(folder_path)

    organizer.organize()
    move_count = organizer.move_count

    # Verify move counts per folder
    assert (
        move_count[str(setup_test_environment / "txt")] == 2
    ), "Two txt files should be moved."
    assert (
        move_count[str(setup_test_environment / "jpg")] == 1
    ), "One jpg file should be moved."
    assert (
        move_count[str(setup_test_environment / "docx")] == 1
    ), "One docx file should be moved."
    assert (
        move_count[str(setup_test_environment / "Duplicates")] == 1
    ), "One duplicate file should be moved."
