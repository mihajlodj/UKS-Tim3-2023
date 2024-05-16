<template>
  <div class="background is-fullheight min-vh-100" style="background-color:#2c333b">
    <RepoNavbar starting="code" />

    <div class="d-flex flex-column justify-content-start w-75 mt-3" style="margin-left:auto; margin-right:auto;">
      <div class="d-flex flex-row">
        <div class="btn-group p-2" role="group" aria-label="Basic radio toggle button group">
          <input type="radio" @change="showDraftAndSearch = true" class="btn-check" name="btnradio"
            id="btnradio-releases" autocomplete="off">
          <label class="btn btn-outline-primary" for="btnradio-releases">Releases</label>

          <input type="radio" @change="showDraftAndSearch = false" class="btn-check" name="btnradio" id="btnradio2"
            autocomplete="off" checked>
          <label class="btn btn-outline-primary" for="btnradio2">Tags</label>
        </div>

        <div class="p-2 ms-auto d-flex flex-row" v-if="showDraftAndSearch">
          <div>

          <button class="btn btn-secondary" style="margin-right: 15px;" data-bs-toggle="modal"
            data-bs-target="#staticBackdrop1">Draft a new release</button>
          </div>
          <div>

          <input type="text" placeholder="Find a release" class="form-control" height="30px;" />
          </div>
        </div>
      </div>

      <hr style="color:#adbbc8;" />

      <div v-if="thereArentAnyTags">
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
              href="https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases"
              target="_blank">our docs.</a><br />
          </h4>
        </div>
      </div>
      <div v-else class="p-2 center">
        <div v-if="showDraftAndSearch === false">
          <ViewTagsComponent :owner="this.owner" :repoName="this.repoName" :tags="this.tags"
            :releases="this.releases" />
        </div>
        <div v-else>
          <ViewReleasesComponent :owner="this.owner" :repoName="this.repoName" :tags="this.tags" :releases="this.releases" :branches="this.branches" />
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="staticBackdrop1" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">New release</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="d-flex flex-row">
              <div class="">
                <button class="btn btn-secondary dropdown-toggle mb-2" type="button" id="dropdownMenuButton"
                  data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <svg data-v-2840cd1c="" class="svg-inline--fa fa-code-branch me-2 mt-1" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="code-branch" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path class="" fill="currentColor" d="M80 104a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm80-24c0 32.8-19.7 61-48 73.3v87.8c18.8-10.9 40.7-17.1 64-17.1h96c35.3 0 64-28.7 64-64v-6.7C307.7 141 288 112.8 288 80c0-44.2 35.8-80 80-80s80 35.8 80 80c0 32.8-19.7 61-48 73.3V160c0 70.7-57.3 128-128 128H176c-35.3 0-64 28.7-64 64v6.7c28.3 12.3 48 40.5 48 73.3c0 44.2-35.8 80-80 80s-80-35.8-80-80c0-32.8 19.7-61 48-73.3V352 153.3C19.7 141 0 112.8 0 80C0 35.8 35.8 0 80 0s80 35.8 80 80zm232 0a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM80 456a24 24 0 1 0 0-48 24 24 0 1 0 0 48z"></path></svg>
                  {{ this.newReleaseBranch == '' ?  'Target branch' : this.newReleaseBranch}}
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <a class="dropdown-item" v-for="(branch, index) in this.branches" :key="index"
                    @click="this.newReleaseBranch = branch.name">{{ branch.name }}</a>
                </div>
              </div>
              <div class="ms-3">
                <button class="btn btn-secondary dropdown-toggle mb-2" type="button" id="dropdownMenuButton"
                  data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="bi bi-tag"></i>{{ this.newTagName == '' ? 'Choose a tag' : this.newTagName }}</button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <a class="dropdown-item" v-for="(tag, index) in this.tags" :key="index"
                    @click="this.newTagName = tag.name">{{ tag.name }}</a>
                  <input type="text" class="dropdown-item form-control" v-model="this.newTagName" placeholder="Enter new tag name" v-on:keydown.enter="setNewTag()"/>
                </div>
              </div>
            </div>
            <input type="text" class="form-control" placeholder="Title" v-model="newReleaseTitle" required/>
            <hr />
            <textarea name="description" id="description" class="form-control"
              placeholder="Describe this release" v-model="newReleaseDescription"></textarea>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" v-model="isPreRelease" id="prerelease">
              <label for="prerelease" class="form-check-label"> Set as pre-release</label>              
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="publishRelease(false)">Publish release</button>
            <button type="button" class="btn btn-secondary" @click="publishRelease(true)">Save draft</button>
          </div>
        </div>
      </div>
    </div>

  </div>

</template>

<script>

import RepoNavbar from '@/components/repository/RepoNavbar.vue';
import ReleaseService from '@/services/ReleaseService';
import TagService from '@/services/TagService';
import ViewTagsComponent from './tag/ViewTagsComponent.vue';
import ViewReleasesComponent from './release/ViewReleasesComponent.vue';
import BranchService from '@/services/BranchService';
import { toast } from 'vue3-toastify';

export default {
  name: 'TagReleaseComponent',
  components: {
    RepoNavbar,
    ViewTagsComponent,
    ViewReleasesComponent
  },
  mounted() {
    this.owner = this.$route.params.ownerUsername;
    this.repoName = this.$route.params.repoName;
    ReleaseService.getReleases(this.owner, this.repoName).then((res) => {
      this.releases = res.data;
      if (res.data != []) {
        this.thereArentAnyTags = false;
      }
    }).catch((err) => {
      console.log('Release service (getReleases) error: ', err);
    });
    TagService.getTags(this.owner, this.repoName).then((res) => {
      this.tags = res.data;
    }).catch((err) => {
      console.log('Tag service (getTags) error: ', err);
    });
    BranchService.getAllBranches(this.owner, this.repoName).then((res) => {
      this.branches = res.data;
    }).catch((err) => {
      console.log('Branch service (getAllBranches) error: ', err);
    });

  },
  data() {
    return {
      newReleaseBranch: '',
      newReleaseDescription: '',
      newReleaseTitle: '',
      isPreRelease: false,
      newTagName: '',
      owner: '',
      repoName: '',

      showDraftAndSearch: false,
      thereArentAnyTags: true,
      releases: [{
        'id': 0,
        'title': '',
        'description': '',
        'branch': {
          'name': undefined,
          'id': undefined
        },
        'pre_release': undefined,
        'draft': undefined,
        'tag': {
          'id': undefined,
          'name': undefined,
        },
        'commit': {
          'hash': '09a9s8ch9218yhh102yhped1',
          'message': undefined,
          'author': {
            'username': undefined
          },
          'timestamp': undefined
        },
        'project': 'repoName'
      }],
      tags: [{
        id: 0,
        name: '',
        caused_by: '',
        commit: {
          hash: '09a9s8ch9218yhh102yhped1',
          message: '',
          timestamp: ''
        }
      }],
      branches: [{
        name: ''
      }],
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
    draftNewRelease() {
      this.$router.push(`/view/${this.owner}/${this.repoName}/releases/releases/new`)
    },
    setNewTag() {

    },
    publishRelease(isDraft) {
      if (this.newTagName == '') {
        toast('Tag name can\'t be blank', this.toastFailed);
        return;
      }
      if (this.newReleaseTitle == '') {
        toast('Title can\'t be blank', this.toastFailed);
        return;
      }
      if (this.newReleaseBranch == '') {
        toast('You must pick a branch', this.toastFailed);
        return;
      }

      let data = {
        title: this.newReleaseTitle,
        description: this.newReleaseDescription,
        branch_name: this.newReleaseBranch,
        pre_release: this.isPreRelease,
        draft: isDraft,
        tag_name: this.newTagName
      }
      ReleaseService.createRelease(this.owner, this.repoName, data).then((res) => {
        console.log(res);
        toast('Draft saved!', this.toastSuccess);
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

.search-releases {
  height: 38px;
  background-color: #2c333b;
  border-radius: 7px;
  border-color: rgba(0, 0, 0, 0);
  color: white;
  outline: none;
}

.search-releases:focus {
  border-color: rgb(42, 109, 255);
  border-width: 5px;
}
</style>