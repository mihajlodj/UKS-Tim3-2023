<template>
    <div v-if="spaces.length > 0" class="d-flex justify-content-center center">
        <div class="d-flex justify-content-start editor">
            <div class="d-flex flex-column line-num">
                <div v-for="(line, index) in lines" :key="line" class="line">
                    <span>{{ index + 1 }}</span>
                </div>
            </div>
            <div class="d-flex flex-column lines">
                <div v-for="(line, index) in lines" :key="line" class="line">
                    <span>
                        <span v-for="n in spaces[index]" :key="n">&nbsp;</span>
                        <span>{{ line }}</span>
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CodeDisplay',

    props: ['lines'],

    /* eslint-disable */
    watch: {
        lines: function (newLines, oldLines) {
            this.countSpaces(newLines);
        }
    },

    data() {
        return {
            spaces: []
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
            console.log(this.spaces);
        }
    }
}
</script>

<style scoped>
.line-num {
    width: 8%;
    max-width: 80px;
    background-color: #22272d;
    color: #adbbc8;
    padding: 15px 15px 15px 60px;
    align-items: end;
    border-top: 1px solid #adbbc8;
    border-bottom: 1px solid #adbbc8;
    border-left: 1px solid #adbbc8;
    border-bottom-left-radius: 7px;
}

.lines {
    width: 92%;
    background-color: #22272d;
    color: white;
    padding: 15px 60px 15px 20px;
    border-top: 1px solid #adbbc8;
    border-bottom: 1px solid #adbbc8;
    border-right: 1px solid #adbbc8;
    border-bottom-right-radius: 7px;
}

.center {
    background-color: #22272d;
}

.editor {
    width: 80%;
}

.line {
    padding: 1px 0px;
    height: 26px;
}
</style>