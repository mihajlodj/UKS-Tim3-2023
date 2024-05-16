<template lang="en">
    <div id="create-form" >
        <div class="mb-3">
            <div class="d-flex flex-column">
                <label class="mb-1" style="color: beige">Name</label>
                <input type="text" v-model="name"/>
            </div>
        </div>
        <div class="mb-2">
            <div class="d-flex flex-column">
                <label class="mb-1" style="color: beige">Description</label>
                <textarea type="text" v-model="description" ></textarea>
            </div>
        </div>
        <div class="flex-container">
            <button type="button" class="btn btn-primary" @click="submit">Edit</button>
        </div>
    </div>
</template>
<script>
import LabelService from '@/services/LabelService'
import { toast } from 'vue3-toastify';

export default {
    name: 'UpdateLabelComponent',

    components: {

    },

    props: ['selectedLabel'],

    mounted() {
        this.label = this.selectedLabel;
        this.setDataFromLabel();
    },

    data() {
        return {
            label: null,
            name: '',
            description: '',
            username: this.$route.params.username,
            repo: this.$route.params.repoName,
        }
    },

    methods: {
        submit() {
            LabelService.updateLabel(this.username, this.repo, this.label.id, {
                "name": this.name,
                "description": this.description,
            }).then((res) => {
                console.log(res);
                toast("Label updated", {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
                this.notifyParrent();
            }).catch((err) => {
                console.log(err);
                toast("Error occured while editing label!", {
                    autoClose: 1000,
                    type: 'error',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            });
        },

        empty_fields() {
            this.name = '';
            this.description = '';
        },

        setDataFromLabel() {
            if (this.label != undefined) {
                this.name = this.label.name;
                this.description = this.label.description;
            }
        },

        notifyParrent() {
            this.$emit('labelUpdated');
        }
    }
}
</script>
<style scoped></style>