<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar />
        <PathDisplay :editing="editing" :key="pathKey" ref="pathDisplay" @updateFileName="updateFileName" />

        <div>
            <NonTextHeader :size="file.size" />
            <div class="d-flex justify-content-center">
                <div class="contain">
                    <object>
                        <embed class="w-100" id="pdfID" type="text/html" height="600"
                            :src="`data:application/pdf;base64,${content}`" />
                    </object>
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
            console.log(this.content);
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
            newFileName: ''
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
</style>