import os

from selene import browser, have, be

from tests.conftest import close_modal


def test_demoqa_form():

    browser.open('/')

    # Убираем баннер и футер, мешающие кнопке Submit
    browser.driver.execute_script("document.querySelector('footer').remove()")

    # Основные поля
    browser.element("#firstName").type('Valeriy')
    browser.element("#lastName").type('Nasyrov')
    browser.element("#userEmail").type('user@example.com')
    browser.element("#gender-radio-1").click()
    browser.element("#userNumber").type('9999999999')

    # Дата рождения
    browser.element('#dateOfBirthInput').should(have.value('23 May 2026'))
    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__month-select').element('option[value="6"]').click()
    browser.element('.react-datepicker__year-select').element('option[value="1993"]').click()
    browser.element('.react-datepicker__day--012').click()
    # browser.element('#dateOfBirthInput').set(value='12 Jul 1993') <<< Альтернативный метод
    browser.element('#dateOfBirthInput').should(have.value('12 Jul 1993'))

    # Subjects
    browser.element('#subjectsInput').should(be.blank)
    browser.element('#subjectsInput').type('Maths')
    close_modal()
    browser.element('#subjectsInput').press_enter()
    browser.element('.subjects-auto-complete__multi-value__label').should(have.text('Maths'))
    browser.element('.subjects-auto-complete__multi-value__remove').click()
    browser.element('#subjectsInput').should(be.blank)
    browser.element('#subjectsInput').type('Maths')
    close_modal()
    browser.element('#subjectsInput').press_enter()

    # .modal-content
    # #closeLargeModal

    #Hobbies
    browser.element('#hobbies-checkbox-1').click()
    browser.element('#hobbies-checkbox-2').click()
    browser.element('#hobbies-checkbox-3').click()
    browser.element('#hobbies-checkbox-1').should(have.js_property('checked', True))
    browser.element('#hobbies-checkbox-1').should(have.js_property('checked', True))
    browser.element('#hobbies-checkbox-1').should(have.js_property('checked', True))

    # Picture
    browser.element('#uploadPicture').send_keys(os.path.abspath('/Users/ivalnasyrov/Desktop/1.jpg'))

    # Current Address
    browser.element("#currentAddress").type('Los Angeles')

    # State
    browser.element('#react-select-3-placeholder').should(have.text('Select State'))
    browser.element('#react-select-3-input').should(have.no.attribute('aria-controls', 'react-select-3-listbox'))
    browser.element('#react-select-3-input').click()
    browser.element('#react-select-3-listbox').should(be.visible)
    browser.element('#react-select-3-listbox').all('[role="option"]'
                    ).should(have.exact_texts('NCR', 'Uttar Pradesh', 'Haryana', 'Rajasthan'))
    browser.element('#city').element('.css-16xfy0z-control'
    ).should(have.attribute('aria-disabled', 'true')) # проверяем что выбор города недоступен до выбора страны
    browser.element('#react-select-3-input').type('Uttar Pradesh').press_enter()
    browser.element('#react-select-3-listbox').should(be.not_.visible)

    # City
    browser.element('#react-select-4-placeholder').should(have.text('Select City'))
    browser.element('#react-select-4-input').should(have.no.attribute('aria-controls', 'react-select-4-listbox'))
    browser.element('#react-select-4-input').click()
    browser.element('#react-select-4-listbox').should(be.visible)
    browser.element('#react-select-4-listbox').all('[role="option"]'
                    ).should(have.exact_texts('Agra', 'Lucknow', 'Merrut'))
    browser.element('#react-select-4-input').type('Agra').press_enter()
    browser.element('#react-select-4-listbox').should(be.not_.visible)

    # Submit
    close_modal()
    browser.element('#submit').click()
    browser.element('.table-responsive').should(be.visible)
    browser.element('#example-modal-sizes-title-lg').should(have.exact_text('Thanks for submitting the form'))
    browser.all('.table-responsive td:nth-child(2)').should(have.exact_texts(

        'Valeriy Nasyrov',
        'user@example.com',
        'Male',
        '9999999999',
        '12 July,1993',
        'Maths',
        'Sports, Reading, Music',
        '1.jpg',
        'Los Angeles',
        'Uttar Pradesh Agra'
    ))