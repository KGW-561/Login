// 'selectAll' 체크박스를 선택
var masterCheckbox = document.getElementById('selectAll');

// 모든 체크박스를 선택
var checkboxes = document.querySelectorAll('input[name="userIds"]');

// 삭제 버튼 선택
var deleteButton = document.getElementById('deleteSubmit');

// 마스터 체크박스 클릭 시 모든 체크박스의 상태를 설정하는 함수
function toggleCheckboxes(master) {
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = master.checked;
  });
}

// 각 체크박스에 변경 이벤트를 추가하여 마스터 체크박스 상태를 업데이트
checkboxes.forEach(function(checkbox) {
  checkbox.addEventListener('change', function() {
    // 모든 체크박스가 선택되었는지 확인
    var allChecked = Array.from(checkboxes).every(function(checkbox) {
      return checkbox.checked;
    });

    // 마스터 체크박스의 상태 업데이트
    masterCheckbox.checked = allChecked;
  });
});

// 마스터 체크박스에 클릭 이벤트 리스너 추가
masterCheckbox.addEventListener('click', function() {
  toggleCheckboxes(masterCheckbox);
});

function collectAndSubmit() {
    // 선택된 체크박스 값 수집
    const selectedIds = Array.from(document.querySelectorAll('input[name="userIds"]:checked'))
                            .map(checkbox => checkbox.value);

    if (selectedIds.length === 0) {
    alert("삭제할 사용자를 선택하세요.");
    return;
    }

    const confirmed = confirm("이 사용자의 계정을 삭제 처리하겠습니까?");

    if (confirmed) {
        alert("계정이 삭제되었습니다.");
          // 숨겨진 필드에 선택된 값 추가
          document.getElementById('userIds').value = selectedIds.join(',');

          // 폼 제출
          document.getElementById('deleteForm').submit();
    } else {
       return; // 폼 제출 막기
    }

}










