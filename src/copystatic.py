import shutil
import os



def copy_function(src, dst):
	if os.path.exists(dst):
		shutil.rmtree(dst)
	os.makedirs(dst, exist_ok=True)
	for entry in os.listdir(src):
		src_path = os.path.join(src, entry)
		dst_path = os.path.join(dst, entry)
		if os.path.isfile(src_path):
			shutil.copy(src_path, dst_path)
			print (f"Copied file: {src_path} -> {dst_path}")
		elif os.path.isdir(src_path):
			os.makedirs(dst_path, exist_ok=True)
			copy_function(src_path, dst_path)
