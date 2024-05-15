<template>
  <div v-if="this.releases.length === 0">
    <div class="center p-2 fs-2">
      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="bi bi-tag text"
        viewBox="0 0 16 16">
        <path d="M6 4.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m-1 0a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0" />
        <path
          d="M2 1h4.586a1 1 0 0 1 .707.293l7 7a1 1 0 0 1 0 1.414l-4.586 4.586a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 1 6.586V2a1 1 0 0 1 1-1m0 5.586 7 7L13.586 9l-7-7H2z" />
      </svg>
    </div>
    <div class="center p-2">
      <h1 class="heading">
        <b>There aren't any releases here</b>
      </h1>
    </div>
    <div class="center p-2 text">
      <h4>
        You can create a release to package software, along with<br />
        release notes and links to binary files, for other people to use.<br />
        Learn more about releases in <a
          href="https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases" target="_blank">our
          docs.</a><br />
      </h4>
    </div>
  </div>

  <table v-else class="table-text-align" style="margin-left: auto; margin-right: auto;">
    <tr class="p-2" v-for="release in this.releases" :key="release.id">
      <td class="p-2 text" style="font-size:18px">
        Caused by: <br />
        {{ release.tag.caused_by }} <br />
        <i class="bi bi-tag"></i>{{ release.tag.name }} <br />
        <i class="bi bi-dash-circle-dotted"></i>{{ release.commit.hash.slice(0, 7) }}
      </td>
      <td width="85%">
        <div class="p-2 card heading shadow-lg" style="background-color:black">
          <h4 class="card-header">{{ release.title }} <span class="badge badge-pill badge-primary"
              :style="release.draft ? 'color:white;' : (release.pre_release ? 'color:orange' : 'color:green')">{{
                release.draft ? 'draft' : (release.pre_release ? 'pre-release' : 'release') }}</span></h4>
          <div class="card-body">
            <p class="card-text">{{ release.description }}</p>
          </div>
          <div class="card-footer">
            Assets:
            <span class="text"><a
                :href="'http://localhost:3000/' + this.owner + '/' + this.repoName + '/archive/' + release.tag.name + '.zip'"><i
                  class="bi bi-file-zip"></i> zip</a></span>
            <span class="text"><a
                :href="'http://localhost:3000/' + this.owner + '/' + this.repoName + '/archive/' + release.tag.name + '.tar.gz'"><i
                  class="bi bi-file-zip"></i> tar.gz</a></span> <br />
            <div class="">
              <button class="btn btn-success m-2" @click="editRelease(release)">Edit
                release</button>
              <button data-bs-target="#staticBackdrop2" id="hidden-button" hidden></button>
              <button class="btn btn-danger m-2" @click="deleteRelease(release)">Delete release</button>
            </div>
          </div>
        </div>
      </td>
    </tr>
  </table>

  <!-- Modal -->
  <div class="modal fade" ref="modal" id="staticBackdrop2" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
    aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="staticBackdropLabel">Edit release</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="d-flex flex-row">
            <div class="">
              <button class="btn btn-secondary dropdown-toggle mb-2" type="button" id="dropdownMenuButton"
                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" disabled>
                <svg data-v-2840cd1c="" class="svg-inline--fa fa-code-branch me-2 mt-1" aria-hidden="true"
                  focusable="false" data-prefix="fas" data-icon="code-branch" role="img"
                  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                  <path class="" fill="currentColor"
                    d="M80 104a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm80-24c0 32.8-19.7 61-48 73.3v87.8c18.8-10.9 40.7-17.1 64-17.1h96c35.3 0 64-28.7 64-64v-6.7C307.7 141 288 112.8 288 80c0-44.2 35.8-80 80-80s80 35.8 80 80c0 32.8-19.7 61-48 73.3V160c0 70.7-57.3 128-128 128H176c-35.3 0-64 28.7-64 64v6.7c28.3 12.3 48 40.5 48 73.3c0 44.2-35.8 80-80 80s-80-35.8-80-80c0-32.8 19.7-61 48-73.3V352 153.3C19.7 141 0 112.8 0 80C0 35.8 35.8 0 80 0s80 35.8 80 80zm232 0a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM80 456a24 24 0 1 0 0-48 24 24 0 1 0 0 48z">
                  </path>
                </svg>
                {{ this.releaseBranch }}
              </button>
            </div>
            <div class="ms-3">
              <button class="btn btn-secondary dropdown-toggle mb-2" type="button" id="dropdownMenuButton"
                data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="bi bi-tag"></i>{{ this.tagName === '' ? 'Choose a tag' : this.tagName }}</button>
              <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" v-for="(tag, index) in this.tags" :key="index"
                  @click="this.tagName = tag.name">{{ tag.name }}</a>
                <input type="text" class="dropdown-item form-control" v-model="this.typedTagName" v-on:keydown="this.tagName = this.typedTagName"
                  placeholder="Enter new tag name" />
              </div>
            </div>
          </div>
          <input type="text" class="form-control" placeholder="Title" v-model="releaseTitle" required />
          <hr />
          <textarea name="description" id="description" class="form-control" placeholder="Describe this release"
            v-model="releaseDescription"></textarea>
          <div class="form-check" style="text-align: left;">
            <input type="checkbox" class="form-check-input" v-model="isPreRelease" id="prerelease" >
            <label for="prerelease" class="form-check-label" style="text-align: left;">Set as pre-release</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="updateRelease(false)">Publish
            release</button>
          <button type="button" class="btn btn-secondary" @click="updateRelease(true)">Save draft</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import ReleaseService from '@/services/ReleaseService';
import { toast } from 'vue3-toastify';
import { Modal } from "bootstrap";

export default {
  name: 'ViewReleasesComponent',
  props: ['owner', 'repoName', 'releases', 'tags', 'branches'],
  mounted() {
    this.modal = new Modal(this.$refs.modal);
  },
  data() {
    return {

      releaseId: 0,
      releaseBranch: '',
      releaseDescription: '',
      releaseTitle: '',
      isPreRelease: false,
      draft: false,
      tagName: '',
      typedTagName: '',

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
    setNewTag() {},
    editRelease(release) {
      this.releaseId = release.id;
      this.releaseBranch = release.branch.name;
      this.releaseDescription = release.description;
      this.releaseTitle = release.title;
      this.isPreRelease = release.pre_release;
      this.tagName = release.tag.name;
      this.draft = release.draft;
      this.modal.show()
    },
    deleteRelease(release) {
      if (confirm('Are you sure you want to delete this release?') == true) {
        ReleaseService.deleteRelease(this.owner, this.repoName, release.tag.name).then((res) => {
          console.log(res);
          toast('Release deleted', this.toastSuccess);
          location.reload()
        }).catch((err) => {
          console.log(err);
          toast('Deletion failed', this.toastFailed);
        });
      }
    },
    updateRelease(isDraft) {
      if (isDraft === true && this.draft === false) {
        toast('Existing release can\'t be turned into a draft', this.toastFailed);
        return;
      }
      if (this.tagName == '') {
        toast('Tag name can\'t be blank', this.toastFailed);
        return;
      }
      if (this.releaseTitle == '') {
        toast('Title can\'t be blank', this.toastFailed);
        return;
      }
      if (this.releaseBranch == '') {
        toast('You must pick a branch', this.toastFailed);
        return;
      }

      let data = {
        release_id: this.releaseId,
        updated_title: this.releaseTitle,
        updated_description: this.releaseDescription,
        branch_name: this.releaseBranch,
        updated_pre_release: this.isPreRelease,
        updated_draft: isDraft,
        updated_tag: this.tagName
      }
      ReleaseService.updateRelease(this.owner, this.repoName, data).then((res) => {
        console.log(res);
        toast('Release updated!', this.toastSuccess);
        location.reload();
      }).catch((err) => {
        console.log(err);
        toast(err.response.data.message, this.toastFailed);
      });
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
</style>