<template>
  <table class="table table-dark table-striped">
    <thead>
      <tr>
        <th scope="col" class="table-text-align heading"><i class="bi bi-tag"></i>Tags</th>
        <th scope="col"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="tag in this.tags" :key="tag.id">
        <td class="table-text-align ">
          <span class="big-text">{{ tag.name }}</span> <br />
          <span class="text"><i class="bi bi-dash-circle-dotted"></i> {{ tag.commit.hash.slice(0, 7) }}</span>
          <span class="text"><a
              :href="'http://localhost:3000/' + this.owner + '/' + this.repoName + '/archive/' + tag.name + '.zip'"><i
                class="bi bi-file-zip"></i> zip</a></span>
          <span class="text"><a
              :href="'http://localhost:3000/' + this.owner + '/' + this.repoName + '/archive/' + tag.name + '.tar.gz'"><i
                class="bi bi-file-zip"></i> tar.gz</a></span>
        </td>
        <td style="text-align: right" v-if="isTagAttachedToRelease(tag)">
          <button class="btn btn-success" style="margin-right: 15px;" @click="editRelease(tag)">Edit the
            release</button>
          <button class="btn btn-secondary" disabled>Delete tag</button>
        </td>
        <td style="text-align: right" v-else>
          <button class="btn btn-success" style="margin-right: 15px;" @click="createRelease(tag)">Create
            release</button>
          <button class="btn btn-danger" @click="deleteTag(tag)">Delete tag</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
<script>

import TagService from '@/services/TagService';
import { toast } from 'vue3-toastify';
export default {
  name: 'ViewTagsComponent',
  props: ['tags', 'owner', 'repoName', 'releases'],
  data() {
    return {
      toastSuccess: {
        autoClose: 1000,
        type: 'success',
        position: toast.POSITION.BOTTOM_RIGHT
      },
      toastFailed: {
        autoClose: 1000,
        type: 'error',
        position: toast.POSITION.BOTTOM_RIGHT
      }
    }
  },
  methods: {
    deleteTag(tag) {
      TagService.deleteTag(this.owner, this.repoName, tag.id).then((res) => {
        console.log(res);
        location.reload();
        toast('Tag deleted', this.toastSuccess);
      }).catch((err) => {
        console.log(err);
        toast('Deletion failed', this.toastFailed);
      })
    },
    isTagAttachedToRelease(tag) {
      let tagId = tag.id;
      let retval = false;
      this.releases.forEach((r) => {
        if (r.tag.id === tagId) {
          retval = true;
        }
      });
      return retval;
    },
    editRelease(tag) {
      this.$router.push(`/view/${this.owner}/${this.repoName}/releases/edit/${tag.name}`)
    },
    createRelease(tag) {
      this.$router.push(`/view/${this.owner}/${this.repoName}/releases/new?=${tag.name}`)
    }
  }
}
</script>
<style scoped>
hr {
  color: #adbbc8;
}

.heading {
  color: white;
}

.center {
  text-align: center;
}

.text {
  color: #848d97;
  font-size: var(--text-body-size-large);
}

.big-text {
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
}

.table-text-align {
  text-align: left;
  margin: auto;
  padding: 10px;
}

th {
  background-color: #161b22;
  height: 50px;
}

input[type=text] {
  height: 38px;
  background-color: #2c333b;
  border-radius: 7px;
  border-color: rgba(0, 0, 0, 0);
  color: white;
  outline: none;
}

input:focus {
  border-color: rgba(0, 0, 255, 1);
  border-width: 5px;
}
</style>