from pathlib import Path
from datetime import datetime
from fastapi import UploadFile, HTTPException, status

storage_dir = Path(__file__).parent.parent / 'storage'

def init_dirs(dirs: list[str] = []) -> None:
   for dir_ in dirs:
      dir_path = storage_dir / dir_
      
      if not dir_path.exists():
         dir_path.mkdir(parents=True)
         print(f'[STORAGE_MANAGER] Created "{dir_path}"')
      else:
         print(f'[STORAGE_MANAGER] Exists "{dir_path}"')

def file_save_to_dir(dirname: str, file: UploadFile) -> str:
   dir_path = storage_dir / dirname
   file_ext = Path(file.filename).suffix
   file_name = file.filename.replace(file_ext, '') + '_' + datetime.now().strftime("%m-%d-%Y_%I-%M_%p") + file_ext.lower()
   file_path = dir_path / file_name

   if not dir_path.exists():
      raise HTTPException(
         status_code = status.HTTP_409_CONFLICT,
         detail = f'Missing directory {dir_path}'
      )
   
   with open(file_path, 'wb') as buffer:
      buffer.write(file.file.read())
      print(f'[STORAGE_MANAGER] File saved as {file_path}')
      return file_name

def file_remove_from_dir(dirname: str, filename: str) -> None:
   dir_path = storage_dir / dirname
   file_path = dir_path / filename
   
   if not file_path.exists():
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'File not found.'
      )
   
   file_path.unlink()

def file_update_from_dir(dirname: str, old_file_name: str, new_file: UploadFile, allowed_exts: list[str]) -> str:
   if not new_file:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = 'Missing new document.'
      )
   
   if not any(new_file.filename.endswith(ext) for ext in allowed_exts):
      raise HTTPException(
         status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
         detail = 'File format is unsupported.'
      )
   
   file_remove_from_dir(dirname, old_file_name)
   return file_save_to_dir(dirname, new_file)

def files_saved_if_all_allowed_and_required(files: list[tuple[str, str, UploadFile, bool, list[str]]] = []) -> tuple[bool, None] | tuple[bool, HTTPException]:
   """Saves provided files if they are supported. Format: [dirname, error_label, uploaded_file, required, allowed_extensions[]]"""
   
   file_names = []
   
   # check invalidity and raise
   for _, file_label, file, required, allowed_exts in files:
      if not file and required:
         raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f'{file_label} is required.'
         )
      
      if file and not any(file.filename.endswith(ext) for ext in allowed_exts):
         raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail = 'File format is unsupported.'
         )
   
   # save and append
   for dirname, _, file, _ in files:
      file_names.append(file_save_to_dir(dirname, file))
   
   return file_names