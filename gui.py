from merger.merger import Merger
import gradio as gr
import os
import tempfile
temp_file = tempfile.NamedTemporaryFile(delete=False)


def merge_subtitles(left_files, right_files, output_folder = None, output_filename = None):
    merger = Merger()
    
    if len(left_files) != len(right_files):
        return "The number of files in the two lists is not the same."
    
    # 파일명만 추출하여 정렬
    left_files = sorted(left_files, key=lambda x: os.path.basename(x.name))
    right_files = sorted(right_files, key=lambda x: os.path.basename(x.name))
    
    # output_folder 값이 비어있거나 None이라면 기본값으로 설정
    if not output_folder:
        output_folder = os.path.join(os.getcwd(), 'outputs')

    merged_files = []
    
    total_files = len(left_files)  # 총 파일 개수
    num_digits = len(str(total_files))  # 총 파일 개수의 자릿수를 계산

    for index, (temp_file1, temp_file2) in enumerate(zip(left_files, right_files)):
        formatted_index = str(index + 1).zfill(num_digits)  # index는 0부터 시작하므로 1을 더해주고, 필요한 만큼 0을 앞에 붙입니다.
        # 이후 formatted_index를 파일 이름 생성에 사용하세요.
        # _TemporaryFileWrapper 객체에서 이름을 얻음
        file1_name = temp_file1.name
        temp_file1_path = temp_file1.name
        temp_file2_path = temp_file2.name
        print('1', temp_file1_path)
        print('2', temp_file2_path)
        if not output_filename:
            temp_filename = f"merged_{os.path.basename(file1_name)}"
        else:
            temp_filename = f"output_filename{formatted_index}"
        # 병합 로직 (이 부분은 `Merger` 클래스의 구현에 따라 다를 수 있습니다)
        merger.merge_files(temp_file1_path, temp_file2_path, output_folder, temp_filename)
        merged_files.append(temp_filename)

    return "\n".join(merged_files)

@staticmethod
def open_folder(folder_path: str):
    if os.path.exists(folder_path):
        os.system(f"start {folder_path}")
    else:
        print(f"The folder {folder_path} does not exist.")


interface = gr.Interface(
    fn=merge_subtitles,
    title = "Merge SRT file1 and file2(This will be executed based on the file name order, not the order of the file list.)",
    inputs=[
        gr.Files(label="file1 to merge(added order will not matter)"),
        gr.Files(label="file2 to merge(need to be same count with file1 files)"),
        gr.Text(label="file directory"),
        gr.Text(label="file name"),
    ],
    outputs=gr.Textbox(label="Result")
             
)


interface.launch()