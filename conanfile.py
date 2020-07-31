from conans import ConanFile, CMake, tools
import shutil


class ZookeeperclientcConan(ConanFile):
    name = "zookeeper-client-c"
    version = "0.1"
    license = "MIT"
    author = "Ivan ipolyiakov@gmail.com"
    url = "https://github.com/powercoderlol/zookeeper-client-c"
    description = "Apache Zookeeper C API library"
    topics = ("zookeeper", "zookeeper-c-api", "zookeeper-c-client")
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = "generated/*"
    src_folder = "./zookeeper/zookeeper-client/zookeeper-client-c"
    short_paths = True

    def source(self):
        self.run("git clone https://github.com/apache/zookeeper.git")
        shutil.move('generated', self.src_folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.src_folder)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/zookeeper", src=self.src_folder + "/include")
        self.copy("*.h", dst="include/zookeeper", src=self.src_folder + "/generated")

        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.copy("zookeeper.lib", dst="lib", src=str(self.settings.build_type), keep_path="False")

    def package_info(self):
        self.cpp_info.libs = ["zookeeper.lib"]
