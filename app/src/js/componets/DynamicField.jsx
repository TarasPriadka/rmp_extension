import React from 'react';
import { Form, Input, Button } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';


export const DynamicFields = (props) => {
    const onFinish = values => {
        if (values.names) {
            console.log('Received values of form:', values);
            props.handleClick(values.names);
        } else {
            console.log('Empty form!');
        }
    };

    return (
        <Form name="dynamic_form_item" className='teacherForm m-4' onFinish={onFinish}>
            <Form.List className="teacherList" name="names">
                {(fields, { add, remove }) => {
                    return (
                        <div>
                            {fields.map((field, index) => (
                                <Form.Item
                                    className='teacherField'
                                    required={false}
                                    key={field.key}
                                >
                                    <Form.Item
                                        {...field}
                                        validateTrigger={['onChange', 'onBlur']}
                                        rules={[
                                            {
                                                required: true,
                                                whitespace: true,
                                                message: "Field can't be empty",
                                            },
                                        ]}
                                        noStyle
                                    >
                                        <Input placeholder="teacher's name" style={{ width: '90%', marginRight: 8 }} />
                                    </Form.Item>         
                                    <MinusCircleOutlined
                                        className="dynamic-delete-button"
                                        onClick={() => {
                                            remove(field.name);
                                        }}
                                    />
                                </Form.Item>
                            ))}
                            <Form.Item>
                                <Button
                                    type="dashed"
                                    className="teacherAdd"
                                    style={{ width: '100%'}}
                                    onClick={() => {
                                        add();
                                    }}
                                >
                                    <PlusOutlined /> Add field
                                </Button>
                            </Form.Item>
                        </div>
                    );
                }}
            </Form.List>

            <Form.Item className='teacherSubmitField'>
                <Button type="primary" className='teacherSubmitButton' htmlType="submit">
                    Submit
        </Button>
            </Form.Item>
        </Form>
    );
};