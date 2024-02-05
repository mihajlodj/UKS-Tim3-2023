<template>
    <div v-if="spaces.length > 0" class="d-flex justify-content-center center">
        <div class="inner-editor">
            <div v-for="(line, index) in lines" :key="line" class="line">
                <span class="line-num">{{ index + 1 }}</span>
                <span class="line-content">
                    <span v-for="n in spaces[index]" :key="n">&nbsp;</span>
                    <span>{{ line }}</span>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CodeDisplay',

    // props: ['lines'],

    // /* eslint-disable */
    // watch: {
    //     lines: function (newLines, oldLines) {
    //         this.countSpaces(newLines);
    //     }
    // },

    mounted() {
        if (localStorage.getItem('fileContent')) {
            this.lines = localStorage.getItem('fileContent').split("\n");
            this.countSpaces(this.lines);
        }
    },    

    data() {
        return {
            spaces: [],
            lines: [],
        }
    },

    methods: {
        countSpaces() {
            for (let i = 0; i < this.lines.length; i++) {
                let li = this.lines[i];
                let counter = 0;
                while (counter < li.length && li[counter] == ' ') {
                    counter++;
                }
                this.spaces.push(counter);
            }
        }
    }
}
</script>

<style scoped>
.line-num {
    width: 100%;
    max-width: 80px;
    background-color: #22272d;
    color: #adbbc8;
    text-align: right;
    padding-right: 10px;
    user-select: none;
}

.line-content {
    background-color: #22272d;
    color: #adbbc8;
    text-align: left;
    padding: 0px 10px 0px 20px;
}

.center {
    background-color: #22272d;
}

.editor {
    width: 80%;
}

.inner-editor {
    display: flex;
    flex-direction: column;
    width: 80%;
    border: 1px solid #adbbc8;
    border-top: none;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
    padding: 15px 0px;
}

.line {
    padding: 1px 0px;
    display: grid;
    grid-template-columns: 1fr 12fr;
}
</style>