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
            <button type="button" class="btn btn-primary" @click="submit">Add</button>
        </div>
    </div>
</template>
<script>
import LabelService from '@/services/LabelService';
import { toast } from 'vue3-toastify';

export default {
    name: 'AddLabelComponent',
    components: {
        
    },

    data() {
        return {
            name: '',
            description: '',
            username: this.$route.params.username,
            repo: this.$route.params.repoName,
        }
    },
    methods: {
        submit() {
            LabelService.createLabel(this.username, this.repo, {
                "name": this.name,
                "description": this.description,
            }).then((res) => {
                console.log(res);
                toast("Label created", {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
                this.empty_fields();
                this.notifyParrent();
            }).catch((err) => {
                console.log(err);
                toast("Error occured while adding new label!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
            });
        },
        empty_fields(){
            this.name = '';
            this.description = '';
        },
        notifyParrent() {
            this.$emit('labelAdded');
        }        
    }
}

</script>
<style scoped></style>