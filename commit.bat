:�C���f�b�N�X�֏グ�āA�R�~�b�g���ă����[�g��push����Ƃ���܂�
:�������@���P�ʂ�commit��
:�������@�C�����̃t�@�C����
:��O�����@�C�����̃\�[�X�R�[�h�ԍ�
:��l�����@�C�����̃\�[�X�R�[�h(1�s)
@set date0=%date:~0,4%%date:~5,2%%date:~8,2%

git status
git add --all .
git status
git commit -m "%date0%_commit_%1" -m "%2_%3_%~4"

:push���邩���肷��B
@set /P ANSWER="push�����s���܂��B��낵���ł����iy/n)?"

@if /i {%ANSWER%}=={y} (goto :yes)
@if /i {%ANSWER%}=={yes} (goto :yes)

@EXIT

:yes
git push origin master