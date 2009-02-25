# Copyright (C) 2009 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Test how Commands are displayed"""

from bzrlib import tests

from bzrlib.plugins.fastimport import (
    commands,
    )


class TestBlobDisplay(tests.TestCase):

    def test_blob(self):
        c = commands.BlobCommand("1", "hello world")
        self.assertEqual("blob\nmark :1\ndata 11\nhello world", repr(c))

    def test_blob_no_mark(self):
        c = commands.BlobCommand(None, "hello world")
        self.assertEqual("blob\ndata 11\nhello world", repr(c))


class TestCheckpointDisplay(tests.TestCase):

    def test_checkpoint(self):
        c = commands.CheckpointCommand()
        self.assertEqual("checkpoint", repr(c))


class TestCommitDisplay(tests.TestCase):

    def test_commit(self):
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        committer = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", "bbb", None, committer,
            "release v1.0", ":aaa", None, None)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "mark :bbb\n"
            "committer Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0\n"
            "from :aaa",
            repr(c))

    def test_commit_unicode_committer(self):
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        name = u'\u013d\xf3r\xe9m \xcdp\u0161\xfam'
        name_utf8 = name.encode('utf8')
        committer = (name, 'test@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", "bbb", None, committer,
            "release v1.0", ":aaa", None, None)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "mark :bbb\n"
            "committer %s <test@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0\n"
            "from :aaa" % (name_utf8,),
            repr(c))

    def test_commit_no_mark(self):
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        committer = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", None, None, committer,
            "release v1.0", ":aaa", None, None)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "committer Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0\n"
            "from :aaa",
            repr(c))

    def test_commit_no_from(self):
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        committer = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", "bbb", None, committer,
            "release v1.0", None, None, None)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "mark :bbb\n"
            "committer Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0",
            repr(c))

    def test_commit_with_author(self):
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        author = ('Sue Wong', 'sue@example.com', 1234565432, -6 * 3600)
        committer = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", "bbb", author,
            committer, "release v1.0", ":aaa", None, None)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "mark :bbb\n"
            "author Sue Wong <sue@example.com> 1234565432 -0600\n"
            "committer Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0\n"
            "from :aaa",
            repr(c))

    def test_commit_with_merges(self):
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        committer = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", "ddd", None, committer,
                "release v1.0", ":aaa", [':bbb', ':ccc'], None)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "mark :ddd\n"
            "committer Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0\n"
            "from :aaa\n"
            "merge :bbb\n"
            "merge :ccc",
            repr(c))

    def test_commit_with_filecommands(self):
        file_cmds = iter([
            commands.FileDeleteCommand('readme.txt'),
            commands.FileModifyCommand('NEWS', 'file', False, None,
                'blah blah blah'),
            ])
        # user tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        committer = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.CommitCommand("refs/heads/master", "bbb", None, committer,
            "release v1.0", ":aaa", None, file_cmds)
        self.assertEqualDiff(
            "commit refs/heads/master\n"
            "mark :bbb\n"
            "committer Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 12\n"
            "release v1.0\n"
            "from :aaa\n"
            "D readme.txt\n"
            "M 644 inline NEWS\n"
            "data 14\n"
            "blah blah blah",
            repr(c))


class TestProgressDisplay(tests.TestCase):

    def test_progress(self):
        c = commands.ProgressCommand("doing foo")
        self.assertEqual("progress doing foo", repr(c))


class TestResetDisplay(tests.TestCase):

    def test_reset(self):
        c = commands.ResetCommand("refs/tags/v1.0", ":xxx")
        self.assertEqual("reset refs/tags/v1.0\nfrom :xxx\n", repr(c))

    def test_reset_no_from(self):
        c = commands.ResetCommand("refs/remotes/origin/master", None)
        self.assertEqual("reset refs/remotes/origin/master", repr(c))


class TestTagDisplay(tests.TestCase):

    def test_tag(self):
        # tagger tuple is (name, email, secs-since-epoch, secs-offset-from-utc)
        tagger = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.TagCommand("refs/tags/v1.0", ":xxx", tagger, "create v1.0")
        self.assertEqual(
            "tag refs/tags/v1.0\n"
            "from :xxx\n"
            "tagger Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 11\n"
            "create v1.0",
            repr(c))

    def test_tag_no_from(self):
        tagger = ('Joe Wong', 'joe@example.com', 1234567890, -6 * 3600)
        c = commands.TagCommand("refs/tags/v1.0", None, tagger, "create v1.0")
        self.assertEqualDiff(
            "tag refs/tags/v1.0\n"
            "tagger Joe Wong <joe@example.com> 1234567890 -0600\n"
            "data 11\n"
            "create v1.0",
            repr(c))


class TestFileModifyDisplay(tests.TestCase):

    def test_filemodify_file(self):
        c = commands.FileModifyCommand("foo/bar", "file", False, ":23", None)
        self.assertEqual("M 644 :23 foo/bar", repr(c))

    def test_filemodify_file_executable(self):
        c = commands.FileModifyCommand("foo/bar", "file", True, ":23", None)
        self.assertEqual("M 755 :23 foo/bar", repr(c))

    def test_filemodify_file_internal(self):
        c = commands.FileModifyCommand("foo/bar", "file", False, None,
            "hello world")
        self.assertEqual("M 644 inline foo/bar\ndata 11\nhello world", repr(c))

    def test_filemodify_symlink(self):
        c = commands.FileModifyCommand("foo/bar", "symlink", False, None, "baz")
        self.assertEqual("M 120000 inline foo/bar\ndata 3\nbaz", repr(c))


class TestFileDeleteDisplay(tests.TestCase):

    def test_filedelete(self):
        c = commands.FileDeleteCommand("foo/bar")
        self.assertEqual("D foo/bar", repr(c))


class TestFileCopyDisplay(tests.TestCase):

    def test_filecopy(self):
        c = commands.FileCopyCommand("foo/bar", "foo/baz")
        self.assertEqual("C foo/bar foo/baz", repr(c))

    def test_filecopy_quoted(self):
        # Check the first path is quoted if it contains spaces
        c = commands.FileCopyCommand("foo/b a r", "foo/b a z")
        self.assertEqual('C "foo/b a r" foo/b a z', repr(c))


class TestFileRenameDisplay(tests.TestCase):

    def test_filerename(self):
        c = commands.FileRenameCommand("foo/bar", "foo/baz")
        self.assertEqual("R foo/bar foo/baz", repr(c))

    def test_filerename_quoted(self):
        # Check the first path is quoted if it contains spaces
        c = commands.FileRenameCommand("foo/b a r", "foo/b a z")
        self.assertEqual('R "foo/b a r" foo/b a z', repr(c))


class TestFileDeleteAllDisplay(tests.TestCase):

    def test_filedeleteall(self):
        c = commands.FileDeleteAllCommand()
        self.assertEqual("deleteall", repr(c))
