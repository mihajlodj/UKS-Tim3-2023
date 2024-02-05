<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar />
        <PathDisplay :editing="editing" :key="pathKey" ref="pathDisplay" @updateFileName="updateFileName" />

        <div>
            <NonTextHeader :size="file.size" @deleteFile="deleteFile" />
            <div class="d-flex justify-content-center">
                <div class="contain">
                    <object v-if="loaded && getFileType() === 'PDF'">
                        <embed class="w-100" type="text/html" height="600"
                            :src="`data:application/pdf;base64,${content}`" />
                    </object>

                    <object v-if="loaded && getFileType() === 'JPG'">
                        <embed class="w-100" type="text/html" height="600" :src="`data:image/jpg;base64,${content}`" />
                    </object>

                    <object v-if="loaded && getFileType() === 'JPEG'">
                        <embed class="w-100" type="text/html" height="600" :src="`data:image/jpeg;base64,${content}`" />
                    </object>

                    <object v-if="loaded && getFileType() === 'PNG'">
                        <embed class="w-100" type="text/html" height="600" :src="`data:image/jpeg;base64,${content}`" />
                    </object>

                    <div v-if="loaded && getFileType() === 'OTHER'" class="d-flex justify-content-center other">
                        <h5 class="my-4">
                            <span>Cannot display file.</span> <span>Download it <a :href="file.download_url">here</a>.</span>
                        </h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import NonTextHeader from './NonTextHeader.vue';
import RepoNavbar from '../RepoNavbar.vue';
import PathDisplay from './PathDisplay.vue';

export default {
    name: "NonTextDisplay",

    components: {
        NonTextHeader,
        RepoNavbar,
        PathDisplay
    },

    mounted() {
        // this.path = this.$route.params.path;
        RepositoryService.getFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.branchName, this.$route.params.path).then(res => {
            this.file = {
                ...res.data
            };
            // this.newFileName = this.file.name;
            this.content = res.data['content'];
            console.log(this.file);
            this.loaded = true;
        }).catch(err => {
            console.log(err);
            // this.allowed = false;
        })
    },

    data() {
        return {
            content: "",
            file: {

            },
            editing: false,
            pathKey: 1,
            newFileName: '',
            loaded: false
        }
    },

    methods: {
        async downloadFile() {
            try {
                const linkSource = `data:application/pdf;base64,${this.content}`;
                const downloadLink = document.createElement("a");
                const fileName = "abc.pdf";
                downloadLink.href = linkSource;
                downloadLink.download = fileName;
                downloadLink.click();
            } catch (error) {
                console.error('Error downloading file', error);
            }
        },

        updateFileName() {

        },

        deleteFile() {
            this.$emit('deleteFile', {});
        },

        getFileType() {
            if (this.file.name.endsWith('.pdf')) return 'PDF';
            if (this.file.name.endsWith('.jpg')) return 'JPG';
            if (this.file.name.endsWith('.jpeg')) return 'JPEG';
            if (this.file.name.endsWith('.png')) return 'PNG';
            return 'OTHER';
        }
    }

}
</script>

<style scoped>
.background {
    background-color: #22272d;
}

.contain {
    width: 80%;
}

h5 {
    color: #adbbc8;
}

.other {
    border: 1px solid #adbbc8;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
}
</style>