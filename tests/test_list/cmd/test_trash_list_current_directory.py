# Copyright (C) 2011 Andrea Francia Trivolzio(PV) Italy

from datetime import datetime

#from tests.support.text.sort_lines import sort_lines
from tests.test_list.cmd.support.trash_list_user import trash_list_user

from tests.support.asserts import assert_equals_with_unidiff
import pytest

class TestTrashListCurrentDirectory:
    @pytest.fixture
    def user(self, trash_list_user):
        u = trash_list_user
        u.set_fake_cwd("/home/user/currentdir")
        return u
    
    @pytest.fixture
    def user_volume(self, trash_list_user):
        u = trash_list_user
        u.add_disk("disk")
        u.set_fake_cwd("/disk/dir1")
        return u
                                   
    def test_currentdir_files_only(self, user):
        user.home_trash_dir().add_trashinfo2('/home/user/currentdir/file1',
                                               datetime(2001, 2, 3, 23, 55, 59))
        user.home_trash_dir().add_trashinfo2('/home/user/otherdir/file2',
                                               datetime(2001, 2, 3, 23, 55, 59))

        result = user.run_trash_list('--currentdir')

        assert_equals_with_unidiff("2001-02-03 23:55:59 " + "/home/user/currentdir/file1\n",
                                   result.stdout)

    def test_currentdir_nested_folders(self, user):
        user.home_trash_dir().add_trashinfo2('/home/user/otherdir/currentdir/file1',
                                               datetime(2001, 2, 3, 23, 55, 59))
        user.home_trash_dir().add_trashinfo2('/home/user/currentdir/newdirectory/file2',
                                               datetime(2001, 2, 3, 23, 55, 59))

        result = user.run_trash_list('--currentdir')

        assert_equals_with_unidiff("2001-02-03 23:55:59 " + "/home/user/currentdir/newdirectory/file2\n",
                                   result.stdout)


    def test_should_output_currendir_should_not_show_currentdir_itself(self, user):
        user.home_trash_dir().add_trashinfo2("/home/user/currentdir",
                                               datetime(2001, 2, 3, 23, 55, 59))
        user.home_trash_dir().add_trashinfo2('/home/user/otherdir/file1',
                                               datetime(2001, 2, 3, 23, 55, 59))

        result = user.run_trash_list('--currentdir')

        assert_equals_with_unidiff("",
                                   result.stdout)
    
    # Same tests but using a different disk
    
    def test_currentdir_files_only(self, user_volume):
        user_volume.home_trash_dir().add_trashinfo2('/disk/dir1/file1',
                                               datetime(2001, 2, 3, 23, 55, 59))
        user_volume.home_trash_dir().add_trashinfo2('/disk/dir2/file2',
                                               datetime(2001, 2, 3, 23, 55, 59))

        result = user_volume.run_trash_list('--currentdir')

        assert_equals_with_unidiff("2001-02-03 23:55:59 " + "/disk/dir1/file1\n",
                                   result.stdout)

    def test_currentdir_nested_folders(self, user_volume):
        user_volume.home_trash_dir().add_trashinfo2('/disk/dir2/dir1/file1',
                                               datetime(2001, 2, 3, 23, 55, 59))
        user_volume.home_trash_dir().add_trashinfo2('/disk/dir1/dir2/file2',
                                               datetime(2001, 2, 3, 23, 55, 59))

        result = user_volume.run_trash_list('--currentdir')

        assert_equals_with_unidiff("2001-02-03 23:55:59 " + "/disk/dir1/dir2/file2\n",
                                   result.stdout)


    def test_should_output_currendir_should_not_show_currentdir_itself(self, user_volume):
        user_volume.home_trash_dir().add_trashinfo2("/disk/dir1",
                                               datetime(2001, 2, 3, 23, 55, 59))
        user_volume.home_trash_dir().add_trashinfo2('/disk1/dir2/file1',
                                               datetime(2001, 2, 3, 23, 55, 59))

        result = user_volume.run_trash_list('--currentdir')

        assert_equals_with_unidiff("",
                                   result.stdout)
