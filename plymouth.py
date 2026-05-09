import os, time, threading

"""

                     $$$$$$\            $$\         $$\ $$\         
                    $$$ __$$\           $$ |      $$$$ |$  |        
 $$$$$$$\  $$$$$$\  $$$$\ $$ | $$$$$$\  $$ |  $$\ \_$$ |\_/$$$$$$$\ 
$$  _____|$$  __$$\ $$\$$\$$ |$$  __$$\ $$ | $$  |  $$ |  $$  _____|
\$$$$$$\  $$ /  $$ |$$ \$$$$ |$$ |  \__|$$$$$$  /   $$ |  \$$$$$$\  
 \____$$\ $$ |  $$ |$$ |\$$$ |$$ |      $$  _$$<    $$ |   \____$$\ 
$$$$$$$  |$$$$$$$  |\$$$$$$  /$$ |      $$ | \$$\ $$$$$$\ $$$$$$$  |
\_______/ $$  ____/  \______/ \__|      \__|  \__|\______|\_______/ 
          $$ |                                                      
          $$ |                                                      
          \__|                                                                                 
  _____  _                             _   _       _                     _ _                _____                          
 |  __ \| |                           | | | |     | |                   | (_)              / ____|                         
 | |__) | |_   _ _ __ ___   ___  _   _| |_| |__   | |     ___   __ _  __| |_ _ __   __ _  | (___   ___ _ __ ___  ___ _ __  
 |  ___/| | | | | '_ ` _ \ / _ \| | | | __| '_ \  | |    / _ \ / _` |/ _` | | '_ \ / _` |  \___ \ / __| '__/ _ \/ _ \ '_ \ 
 | |    | | |_| | | | | | | (_) | |_| | |_| | | | | |___| (_) | (_| | (_| | | | | | (_| |  ____) | (__| | |  __/  __/ | | |
 |_|    |_|\__, |_| |_| |_|\___/ \__,_|\__|_| |_| |______\___/ \__,_|\__,_|_|_| |_|\__, | |_____/ \___|_|  \___|\___|_| |_|
            __/ |                                                                   __/ |                                  
           |___/                                                                   |___/                                   
		  
sp0rk1s Plymouth Loading Screen
1.0.1

"""

class PlymouthJob:

	name: str
	description: str
	progress: int
	complete: bool
	status: str
	started: int
	thread: threading.Thread
	plymouth: 'Plymouth'

	def __init__(self, plymouth: 'Plymouth', name: str, description: str):
		self.plymouth = plymouth
		self.plymouth.print(f"         \033[90mStarting \033[0m{name}\033[90m - {description}...\033[0m")
		self.name = name
		self.description = description
		self.started = time.time()
		self.status = "starting"

		self.thread = threading.Thread(target=self._routine, daemon=True)
		self.thread.start()

	def _routine(self):
		_PATTERN: list[str] = [
			f"\033[0;31m*     ",
			f"\033[1;31m*\033[0;31m*    ",
			f"\033[0;31m*\033[1;31m*\033[0;31m*   ",
			f" \033[0;31m*\033[1;31m*\033[0;31m*  ",
			f"  \033[0;31m*\033[1;31m*\033[0;31m* ",
			f"   \033[0;31m*\033[1;31m*\033[0;31m*",
			f"    \033[1;31m*\033[0;31m*",
			f"     \033[0;31m*",
			f"    \033[1;31m*\033[0;31m*",
			f"   \033[0;31m*\033[1;31m*\033[0;31m*",
			f"  \033[0;31m*\033[1;31m*\033[0;31m* ",
			f" \033[0;31m*\033[1;31m*\033[0;31m*  ",
			f"\033[0;31m*\033[1;31m*\033[0;31m*   ",
			f"\033[1;31m*\033[0;31m*    ",
			f"\033[0;31m*     ",
		]
		self.plymouth.print(f"\033[90m[\033[32m  OK  \033[90m] Started \033[0m{self.name}\033[90m - {self.description}.\033[0m")
		self.status = "started"
		while self.status == "started":
			if 5 < time.time() - self.started:
				self.status = "highlighted"
			time.sleep(0.2)

		if self.status == "highlighted":
			line = self.plymouth.print(f"\033[90m[      \033[90m] Job {self.name} running (5s / no limit)\033[0m")
			while self.status == "highlighted":
				elapsed = time.time() - self.started
				pattern = _PATTERN[int(elapsed*2 % len(_PATTERN))]
				self.plymouth.update(line, f"\033[90m[{pattern}\033[90m] Job {self.name} running ({int(elapsed)}s / no limit)\033[0m")
				time.sleep(0.5)
			self.plymouth.update(line, f"\033[90m[      \033[90m] Job {self.name} running ({int(elapsed)}s / no limit)\033[0m")
				
		if self.status == "finished":
			self.plymouth.print(f"\033[90m[\033[32m  OK  \033[90m] Finished \033[0m{self.name}\033[90m - {self.description}.\033[0m")
		if self.status == "depend":
			self.plymouth.print(f"\033[90m[\033[33mDEPEND\033[90m] Dependent \033[0m{self.name}\033[90m - {self.description}.\033[0m")
		if self.status == "warned":
			self.plymouth.print(f"\033[90m[\033[33m WARN \033[90m] Warned \033[0m{self.name}\033[90m - {self.description}.\033[0m")
		if self.status == "failed":
			self.plymouth.print(f"\033[90m[\033[31mFAILED\033[90m] Failed \033[0m{self.name}\033[90m - {self.description}.\033[0m")

	def finish(self) -> None:
		self.status = "finished"

	def depend(self) -> None:
		self.status = "depend"

	def warn(self) -> None:
		self.status = "warned"

	def fail(self) -> None:
		self.status = "failed"


class Plymouth:

	jobs: dict[str, PlymouthJob]
	lines: int
	_os: str
	_clear: bool

	def __init__(self, clear = True):
		self.lines = 0
		job = PlymouthJob(self, "init@plymouth", "Initiating Plymouth loading screen")
		import os
		os.system("color")
		self._clear = clear
		self._os = os.name
		if self._clear and self._os == "nt":
			os.system("cls")
		elif self._clear and self._os == "posix":
			os.system("clear")
		elif self._clear:
			os.system("clear")
		self.jobs = {"Plymouth": job}
		job.finish()

	def print(self, message: str) -> int:
		print(message)
		self.lines += 1
		return self.lines - 1
	
	def info(self, message: str) -> None:
		self.print(f"         \033[90m{message}\033[0m")

	def update(self, line, message: str) -> None:
		print(f"\033[s\033[{line - self.lines + 1}A\033[90m{message}\033[u", end = "", flush = True)

	def start(self, name: str, description: str) -> PlymouthJob:
		job = PlymouthJob(self, name, description)
		self.jobs[name] = job
		time.sleep(0.01)
		return job
	
	def end(self):
		for job in self.jobs.values():
			if job.status in ["starting", "started", "highlighted"]:
				job.fail()
				job.thread.join()
		job = PlymouthJob(self, "end@plymouth", "All jobs finished, ending Plymouth loading screen")
		time.sleep(0.5)
		job.finish()
		time.sleep(0.1)
		if self._clear and self._os == "nt":
			os.system("cls")
		elif self._clear and self._os == "posix":
			os.system("clear")
		elif self._clear:
			os.system("clear")
